import ast
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import requests,json
global db,cursor,API_key
import pickle
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import random
import torch
import torch.nn as nn
from pathlib import Path
db = pymysql.connect(host='localhost', user='root', password='iamzain')
cursor = db.cursor()
sql = '''use kryptonite'''
cursor.execute(sql)
API_key= '69a4a424b71c68ab389328ba828f71f2'

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

def recommend_collaborative(id,similarity_scores,pt):
    try:
        index = np.where(pt.index == id)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:50]
        newlist = []
        for i in similar_items:
            newlist.append(pt.index[i[0]])
        return newlist

    except:
        return 0

def implicitcollaborativerecommendations(movieIDs,userID):
    tmdblist = []
    recommendations = []
    for i in movieIDs:
        tmdblist.append(i[0])
    pt= pickle.load(open('pt_implicit.pkl', 'rb'))
    similarity = pickle.load(open('similarity_scores_collaborative_implicit.pkl', 'rb'))
    for i in tmdblist:
        recommendations.append(recommend_collaborative(i, similarity,pt))
    for i in recommendations[0]:
        try:
            contentquery = "INSERT INTO user_recommendations values(%s,%s,%s,SYSDATE())" % (int(userID), int(i), 2)
            cursor.execute(contentquery)
            db.commit()
        except:
            pass

def explicitcollaborativerecommendations(movieIDs,userID):
    tmdblist = []
    recommendations = []
    for i in movieIDs:
        tmdblist.append(i[0])
    pt= pickle.load(open('pt_explicit.pkl', 'rb'))
    similarity = pickle.load(open('similarity_scores_collaborative_explicit.pkl', 'rb'))
    for i in tmdblist:
        recommendations.append(recommend_collaborative(i, similarity,pt))
    for i in recommendations[0]:
        try:
            contentquery = "INSERT INTO user_recommendations values(%s,%s,%s,SYSDATE())" % (int(userID), int(i), 3)
            cursor.execute(contentquery)
            db.commit()
        except:
            pass

def explicitneuralcollaborativerecommendations(userID):
    loadedmodel = torch.load('ncf_explicit.pth')
    ratings=pd.read_csv('rating_explicit.csv')
    all_movieIds = ratings['tmdbID'].unique()
    user_interacted_items = ratings.groupby('userID')['tmdbID'].apply(list).to_dict()
    interacted_items = user_interacted_items[userID]
    not_interacted_items = set(all_movieIds) - set(interacted_items)
    selected_not_interacted = list(np.random.choice(list(not_interacted_items), 100))
    test_items = selected_not_interacted
    predicted_labels = np.squeeze(loadedmodel(torch.tensor([userID] * 100), torch.tensor(test_items)).detach().numpy())
    top_items = [test_items[i] for i in np.argsort(predicted_labels)[::-1][0:30].tolist()]
    for i in top_items:
        try:
            contentquery = "INSERT INTO user_recommendations values(%s,%s,%s,SYSDATE())" % (int(userID), int(i), 5)
            cursor.execute(contentquery)
            db.commit()
        except:
            pass


def implicitneuralcollaborativerecommendations(userID):
    loadedmodel = torch.load('ncf_implicit.pth')
    ratings=pd.read_csv('rating_implicit.csv')
    movieinfo=[]
    all_movieIds = ratings['tmdbID'].unique()
    user_interacted_items = ratings.groupby('userID')['tmdbID'].apply(list).to_dict()
    userID = int(userID)
    interacted_items = user_interacted_items[userID]
    not_interacted_items = set(all_movieIds) - set(interacted_items)
    selected_not_interacted = list(np.random.choice(list(not_interacted_items), 100))
    test_items = selected_not_interacted
    predicted_labels = np.squeeze(loadedmodel(torch.tensor([userID] * 100), torch.tensor(test_items)).detach().numpy())
    top_items = [test_items[i] for i in np.argsort(predicted_labels)[::-1][0:30].tolist()]
    for i in top_items:
        try:
            contentquery = "INSERT INTO user_recommendations values(%s,%s,%s,SYSDATE())" % (int(userID), int(i), 4)
            cursor.execute(contentquery)
            db.commit()
        except:
            pass

def generate_recommendations():
    useridlistimp=[]
    getuserIdquery='SELECT DISTINCT userID FROM rating_implicit where userid>980;'
    cursor.execute(getuserIdquery)
    userIDs=cursor.fetchall()
    for i in userIDs:
        useridlistimp.append(i[0])
    for userimp in useridlistimp:
        getmoviequery = 'select tmdbID from rating_implicit WHERE userID = %s;' % (userimp)
        cursor.execute(getmoviequery)
        movieIDs = cursor.fetchall()
        implicitcollaborativerecommendations(movieIDs,userimp)
        implicitneuralcollaborativerecommendations(userimp)
    useridlistexp = []
    getuserIdquery = 'SELECT DISTINCT userID FROM rating_explicit where userid>980;'
    cursor.execute(getuserIdquery)
    userIDs = cursor.fetchall()
    for i in userIDs:
        useridlistexp.append(i[0])
    for userexp in useridlistexp:
        getmoviequery = 'select tmdbID from rating_explicit WHERE userID = %s;' % (userexp)
        cursor.execute(getmoviequery)
        movieIDs = cursor.fetchall()
        explicitcollaborativerecommendations(movieIDs, userexp)
        explicitneuralcollaborativerecommendations(userexp)


generate_recommendations()