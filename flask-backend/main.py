import pymysql
import requests,json
global db,cursor,API_key
import pickle
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
from torch import nn
from torch.utils.data import Dataset, DataLoader
import torch
from pathlib import Path
from tqdm.notebook import tqdm


db = pymysql.connect(host='localhost', user='root', password='iamzain')
cursor = db.cursor()
sql = '''use kryptonite'''
cursor.execute(sql)

def save_model(model: torch.nn.Module,
               target_dir: str,
               model_name: str):
    # Create target directory
    target_dir_path = Path(target_dir)
    target_dir_path.mkdir(parents=True,
                        exist_ok=True)

    # Create model save path
    assert model_name.endswith(".pth") or model_name.endswith(".pt"), "model_name should end with '.pt' or '.pth'"
    model_save_path = target_dir_path / model_name

    # Save the model state_dict()
    print(f"[INFO] Saving model to: {model_save_path}")
    torch.save(obj=model.state_dict(),
             f=model_save_path)

def generate_train_content_data():
    sql = '''SELECT * FROM train_content_data'''
    cursor.execute(sql)
    data = cursor.fetchall()
    movieID = []
    tmdbID = []
    title = []
    release_year = []
    overview = []
    for i in data:
        movieID.append(i[0])
        title.append(i[1])
        release_year.append((i[2]))
        overview.append(i[3])
        tmdbID.append(i[4])
    content_based_data = pd.DataFrame(movieID, columns=["movieID"])
    content_based_data["title"] = title
    content_based_data["release_year"] = release_year
    content_based_data['overview'] = overview
    content_based_data["tmdbID"] = tmdbID
    content_based_data.to_csv('content_based_data.csv', index=False)
    ps = PorterStemmer()
    new_df = pd.read_csv('content_based_data.csv')

    def stem(text):
        x = []
        for i in text.split():
            x.append(ps.stem(i))
        return " ".join(x)

    new_df.overview = new_df.overview.apply(stem)
    new_df.overview = new_df.overview.apply(lambda x: x.lower())
    cv = CountVectorizer(max_features=3000, stop_words='english')
    vectors = cv.fit_transform(new_df.overview).toarray()
    global similarity_scores_content
    similarity_scores_content = cosine_similarity(vectors)
    pickle.dump(similarity_scores_content, open('similarity_scores_content.pkl', 'wb'))
    pickle.dump(content_based_data, open('pt_content.pkl', 'wb'))

def generate_train_collaborative_implicit_data():
    sql = '''SELECT * FROM rating_implicit'''
    cursor.execute(sql)
    data = cursor.fetchall()
    userID = []
    tmdbID = []
    interaction = []
    timestamp = []
    for i in data:
        userID.append(i[0])
        tmdbID.append(i[1])
        interaction.append(i[2])
        timestamp.append(i[3])
    rating_implicit = pd.DataFrame(userID, columns=["userID"])
    rating_implicit["tmdbID"] = tmdbID
    rating_implicit["interaction"] = interaction
    rating_implicit["timestamp"] = timestamp
    rating_implicit.to_csv('rating_implicit.csv', index=False)
    ratings = pd.read_csv('rating_implicit.csv')
    x = ratings.groupby('userID').count()['interaction'] > 1
    active_users = x[x].index
    filtered_rating = ratings[ratings['userID'].isin(active_users)]
    y = filtered_rating.groupby('tmdbID').count()['interaction'] >= 1
    famous_movies = y[y].index
    final_ratings = filtered_rating[filtered_rating['tmdbID'].isin(famous_movies)]
    pt = final_ratings.pivot_table(index='tmdbID', columns='userID', values='interaction')
    pt.fillna(0, inplace=True)
    global similarity_scores_collaborative_implicit
    similarity_scores_collaborative_implicit = cosine_similarity(pt)
    pickle.dump(similarity_scores_collaborative_implicit, open('similarity_scores_collaborative_implicit.pkl', 'wb'))
    pickle.dump(pt, open('pt_implicit.pkl', 'wb'))

def generate_train_collaborative_explicit_data():
    sql = '''SELECT * FROM rating_explicit'''
    cursor.execute(sql)
    data = cursor.fetchall()
    userID = []
    tmdbID = []
    rating = []
    timestamp = []
    for i in data:
        userID.append(i[0])
        tmdbID.append(i[1])
        rating.append(i[2])
        timestamp.append(i[3])
    rating_explicit = pd.DataFrame(userID, columns=["userID"])
    rating_explicit["tmdbID"] = tmdbID
    rating_explicit['rating'] = rating
    rating_explicit["timestamp"] = timestamp
    rating_explicit.to_csv('rating_explicit.csv', index=False)
    ratings=pd.read_csv('rating_explicit.csv')
    x = ratings.groupby('userID').count()['rating'] > 1
    active_users = x[x].index
    filtered_rating = ratings[ratings['userID'].isin(active_users)]
    y = filtered_rating.groupby('tmdbID').count()['rating'] >= 1
    famous_movies = y[y].index
    final_ratings = filtered_rating[filtered_rating['tmdbID'].isin(famous_movies)]
    pt = final_ratings.pivot_table(index='tmdbID', columns='userID', values='rating')
    pt.fillna(0, inplace=True)
    global similarity_scores_collaborative_explicit
    similarity_scores_collaborative_explicit = cosine_similarity(pt)
    pickle.dump(similarity_scores_collaborative_explicit, open('similarity_scores_collaborative_explicit.pkl', 'wb'))
    pickle.dump(pt, open('pt_explicit.pkl', 'wb'))

class MovieLensTrainDataset(Dataset):
    """MovieLens PyTorch Dataset for Training

    Args:
        ratings (pd.DataFrame): Dataframe containing the movie ratings
        all_movieIds (list): List containing all movieIds

    """

    def __init__(self, ratings, all_movieIds):
        self.users, self.items, self.labels = self.get_dataset(ratings, all_movieIds)

    def __len__(self):
        return len(self.users)

    def __getitem__(self, idx):
        return self.users[idx], self.items[idx], self.labels[idx]

    def get_dataset(self, ratings, all_movieIds):
        users, items, labels = [], [], []
        user_item_set = set(zip(ratings['userID'], ratings['tmdbID']))

        num_negatives = 1
        for u, i in user_item_set:
            users.append(u)
            items.append(i)
            labels.append(1)
            for _ in range(num_negatives):
                negative_item = np.random.choice(all_movieIds)
                while (u, negative_item) in user_item_set:
                    negative_item = np.random.choice(all_movieIds)
                users.append(u)
                items.append(negative_item)
                labels.append(0)

        return torch.tensor(users), torch.tensor(items), torch.tensor(labels)


class NCF_Implicit(nn.Module):
    """ Neural Collaborative Filtering (NCF)

        Args:
            num_users (int): Number of unique users
            num_items (int): Number of unique items
            ratings (pd.DataFrame): Dataframe containing the movie ratings for training
            all_movieIds (list): List containing all movieIds (train + test)
    """

    def __init__(self, num_users, num_items, ratings, all_movieIds):
        super().__init__()
        self.user_embedding = nn.Embedding(num_embeddings=num_users, embedding_dim=8)
        self.item_embedding = nn.Embedding(num_embeddings=num_items, embedding_dim=8)
        self.fc1 = nn.Linear(in_features=16, out_features=64)
        self.fc2 = nn.Linear(in_features=64, out_features=128)
        self.fc3 = nn.Linear(in_features=128, out_features=32)
        self.output = nn.Linear(in_features=32, out_features=1)
        self.ratings = ratings
        self.all_movieIds = all_movieIds

    def forward(self, user_input, item_input):
        # Pass through embedding layers
        user_embedded = self.user_embedding(user_input)
        item_embedded = self.item_embedding(item_input)

        # Concat the two embedding layers
        vector = torch.cat([user_embedded, item_embedded], dim=-1)

        # Pass through dense layer
        vector = nn.ReLU()(self.fc1(vector))
        vector = nn.ReLU()(self.fc2(vector))
        vector = nn.ReLU()(self.fc3(vector))

        # Output layer
        pred = nn.Sigmoid()(self.output(vector))

        return pred

def generate_train_neuralcollaborative_implicit_data():
    sql = '''SELECT * FROM rating_implicit'''
    cursor.execute(sql)
    data = cursor.fetchall()
    userID = []
    tmdbID = []
    interaction = []
    timestamp = []
    for i in data:
        userID.append(i[0])
        tmdbID.append(i[1])
        interaction.append(i[2])
        timestamp.append(i[3])
    rating_implicit = pd.DataFrame(userID, columns=["userID"])
    rating_implicit["tmdbID"] = tmdbID
    rating_implicit["interaction"] = interaction
    rating_implicit["timestamp"] = timestamp
    rating_implicit.to_csv('rating_implicit.csv', index=False)
    device = "cpu"
    ratings = pd.read_csv('rating_implicit.csv', parse_dates=['timestamp'])
    rand_userIds = np.random.choice(ratings['userID'].unique(), size=int(len(ratings['userID'].unique()) * 1.0),
                                    replace=False)
    ratings = ratings.loc[ratings['userID'].isin(rand_userIds)]
    ratings['rank_latest'] = ratings.groupby(['userID'])['timestamp'].rank(method='first', ascending=False)
    train_ratings = ratings
    # test_ratings = ratings[ratings['rank_latest'] == 1]
    train_ratings = train_ratings[['userID', 'tmdbID', 'interaction']]
    # test_ratings = test_ratings[['userId', 'movieId', 'rating']]
    train_ratings.loc[:, 'interaction'] = 1

    all_movieIds = ratings['tmdbID'].unique()
    users, items, labels = [], [], []
    user_item_set = set(zip(train_ratings['userID'], train_ratings['tmdbID']))
    num_negatives = 1
    for (u, i) in tqdm(user_item_set):
        users.append(u)
        items.append(i)
        labels.append(1)
        for _ in range(num_negatives):
            negative_item = np.random.choice(all_movieIds)
            while (u, negative_item) in user_item_set:
                negative_item = np.random.choice(all_movieIds)
            users.append(u)
            items.append(negative_item)
            labels.append(0)
    train_dataloader = DataLoader(MovieLensTrainDataset(ratings, all_movieIds), batch_size=64)
    test_dataloader = DataLoader(MovieLensTrainDataset(ratings, all_movieIds), batch_size=64)
    num_users = ratings['userID'].max() + 1
    num_items = ratings['tmdbID'].max() + 1
    all_movieIds = ratings['tmdbID'].unique()
    model = NCF_Implicit(num_users, num_items, train_ratings, all_movieIds)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = torch.nn.BCELoss()
    losses = []
    for epoch in range(2):
        for batch_idx, (user_input, item_input, labels) in enumerate(train_dataloader):
            predicted_labels = model(user_input, item_input)
            loss = nn.BCELoss()(predicted_labels, labels.view(-1, 1).float())
            losses.append(loss.item())
            model.zero_grad()
            loss.backward()
            optimizer.step()
    torch.save(model, 'ncf_implicit.pth')

def generate_train_neuralcollaborative_explicit_data():
    sql = '''SELECT * FROM rating_explicit'''
    cursor.execute(sql)
    data = cursor.fetchall()
    userID = []
    tmdbID = []
    rating = []
    timestamp = []
    for i in data:
        userID.append(i[0])
        tmdbID.append(i[1])
        rating.append(i[2])
        timestamp.append(i[3])
    rating_explicit = pd.DataFrame(userID, columns=["userID"])
    rating_explicit["tmdbID"] = tmdbID
    rating_explicit['rating'] = rating
    rating_explicit["timestamp"] = timestamp
    rating_explicit.to_csv('rating_explicit.csv', index=False)
    device = "cpu"
    ratings = pd.read_csv('rating_explicit.csv', parse_dates=['timestamp'])
    rand_userIds = np.random.choice(ratings['userID'].unique(), size=int(len(ratings['userID'].unique()) * 1.0),
                                    replace=False)
    ratings = ratings.loc[ratings['userID'].isin(rand_userIds)]
    # print('There are {} rows of data from {} users'.format(len(ratings), len(rand_userIds)))
    ratings['rank_latest'] = ratings.groupby(['userID'])['timestamp'].rank(method='first', ascending=False)
    train_ratings = ratings
    # test_ratings = ratings[ratings['rank_latest'] == 1]
    train_ratings = train_ratings[['userID', 'tmdbID', 'rating']]
    # test_ratings = test_ratings[['userId', 'movieId', 'rating']]
    newratings = []
    for i in range(0, len(train_ratings.loc[:, 'rating'].values)):
        if (train_ratings.loc[:, 'rating'].values[i] > 2):
            newratings.append(1)
        else:
            newratings.append(0)
    train_ratings = train_ratings.drop(columns=['rating'])
    train_ratings['rating'] = newratings
    from tqdm.notebook import tqdm
    all_movieIds = ratings['tmdbID'].unique()
    users, items, labels = [], [], []
    user_item_set = set(zip(train_ratings['userID'], train_ratings['tmdbID']))
    num_negatives = 1
    for (u, i) in tqdm(user_item_set):
        users.append(u)
        items.append(i)
        labels.append(1)
        for _ in range(num_negatives):
            negative_item = np.random.choice(all_movieIds)
            while (u, negative_item) in user_item_set:
                negative_item = np.random.choice(all_movieIds)
            users.append(u)
            items.append(negative_item)
            labels.append(0)
    train_dataloader = DataLoader(MovieLensTrainDataset(ratings, all_movieIds), batch_size=64)
    test_dataloader = DataLoader(MovieLensTrainDataset(ratings, all_movieIds), batch_size=64)
    num_users = ratings['userID'].max() + 1
    num_items = ratings['tmdbID'].max() + 1
    all_movieIds = ratings['tmdbID'].unique()
    model = NCF_Implicit(num_users, num_items, train_ratings, all_movieIds)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = torch.nn.BCELoss()
    losses = []
    for epoch in range(2):
        for batch_idx, (user_input, item_input, labels) in enumerate(train_dataloader):
            predicted_labels = model(user_input, item_input)
            loss = nn.BCELoss()(predicted_labels, labels.view(-1, 1).float())
            losses.append(loss.item())
            model.zero_grad()
            loss.backward()
            optimizer.step()
    torch.save(model, 'ncf_explicit.pth')


# generate_train_content_data()
generate_train_neuralcollaborative_explicit_data()
generate_train_neuralcollaborative_implicit_data()
# generate_train_collaborative_explicit_data()
# generate_train_collaborative_implicit_data()
