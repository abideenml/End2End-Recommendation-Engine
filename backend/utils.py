import pickle
import requests
import json
from . import database
from . import config
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

cursor, db = database.get_db()
API_key = config.TMDB_API_KEY

def recommend_content(id,similarity,tmdblist):
    newid=0
    for i, x in enumerate(tmdblist):
        if x==id:
            newid=i
            distances = similarity[newid]
            movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:5]
            newlist = []
            for i in movie_list:
                newlist.append(tmdblist[i[0]])
            return newlist


def contentrecommendations(movieIDs,userID):
    tmdblist = []
    recommendations = []
    movieinfo=[]
    for i in movieIDs:
        tmdblist.append(i[0])
    tmdblist = [*set(tmdblist)]
    similarity = pickle.load(open('similarity_scores_content.pkl', 'rb'))
    contentbaseddata=pd.read_csv('content_based_data.csv')
    tmdbidlist=contentbaseddata.tmdbID
    for i in tmdblist:
        recommendations.append(recommend_content(i, similarity,tmdbidlist))
    for i in recommendations:
        for j in i:
            contentquery = "INSERT INTO user_recommendations values(%s,%s,%s,SYSDATE())"%(int(userID), int(j), 1)
            cursor.execute(contentquery)
            db.commit()
            x = get_data(j)
            if x != 0:
                movieinfo.append(x)
    return movieinfo

def implicitcollaborativerecommendations(userID):
    recommendations=[]
    movieinfo=[]
    getrecommendationsquery = 'SELECT DISTINCT tmdbID FROM user_recommendations WHERE userID=%s AND modelID=%s;'%(userID,2)
    cursor.execute(getrecommendationsquery)
    movies = cursor.fetchall()
    for i in movies:
        recommendations.append(i[0])
    for i in recommendations[:7]:
        try:
            x = get_data(i)
            if x != 0:
                movieinfo.append(x)
        except:
            pass
    return movieinfo

def explicitcollaborativerecommendations(userID):
    recommendations = []
    movieinfo = []
    getrecommendationsquery = 'SELECT DISTINCT tmdbID FROM user_recommendations WHERE userID=%s AND modelID=%s;' % (userID,3)
    cursor.execute(getrecommendationsquery)
    movies = cursor.fetchall()
    for i in movies:
        recommendations.append(i[0])
    for i in recommendations[:7]:
        try:
            x = get_data(i)
            if x != 0:
                movieinfo.append(x)
        except:
            pass
    return movieinfo

def explicitneuralcollaborativerecommendations(userID):
    recommendations = []
    movieinfo = []
    getrecommendationsquery = 'SELECT DISTINCT tmdbID FROM user_recommendations WHERE userID=%s AND modelID=%s;' % (userID,5)
    cursor.execute(getrecommendationsquery)
    movies = cursor.fetchall()
    for i in movies:
        recommendations.append(i[0])
    for i in recommendations[:7]:
        try:
            x = get_data(i)
            if x != 0:
                movieinfo.append(x)
        except:
            pass
    return movieinfo


def implicitneuralcollaborativerecommendations(userID):
    recommendations = []
    movieinfo = []
    getrecommendationsquery = 'SELECT DISTINCT tmdbID FROM user_recommendations WHERE userID=%s AND modelID=%s;' % (userID,4)
    cursor.execute(getrecommendationsquery)
    movies = cursor.fetchall()
    for i in movies:
        recommendations.append(i[0])
    for i in recommendations[:7]:
        try:
            x = get_data(i)
            if x != 0:
                movieinfo.append(x)
        except:
            pass
    return movieinfo



def get_data(Movie_ID):
    query = 'https://api.themoviedb.org/3/movie/'+str(Movie_ID)+'?api_key='+ API_key +'&language=en-US'
    response =  requests.get(query)
    if response.status_code==200:
        array = response.json()
        text = json.dumps(array)
        dataset = json.loads(text)
        if (dataset['backdrop_path'] == None):
            return 0
        return dataset
    else:
        return 0
def fetchmylist(movieids):
    mylist=[]
    for i in movieids:
        x=get_data(i[0])
        if x!=0:
            mylist.append(x)

    return mylist



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

