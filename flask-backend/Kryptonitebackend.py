import ast
from dotenv import load_dotenv
import os
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
import random
load_dotenv()

db = pymysql.connect(host='localhost', user='root', password='iamzain1')
cursor = db.cursor()
sql = '''use kryptonite'''
cursor.execute(sql)
API_key= '69a4a424b71c68ab389328ba828f71f2'


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
    query = 'https://api.themoviedb.org/3/movie/'+str(Movie_ID)+'?api_key='+API_key+'&language=en-US'
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


app = Flask(__name__)
CORS(app)
@app.route('/register',methods=['POST'])
def register():
    data = request.get_data()
    data= data.decode('utf-8')
    data = ast.literal_eval(data)
    name = data[0]
    age = data[1]
    age=int(age)
    if age<1:
        age=1
    email = data[2]
    password = data[3]
    print(name,email)
    registerquery = "INSERT INTO users (name,age,email,password) values('%s',%s,'%s', '%s')"% (name,age,email, password)
    cursor.execute(registerquery)
    db.commit()
    return ""

@app.route('/getuserIdsignin',methods=['GET'])
def getuserIdsignin():
    args = request.args
    email = args['email']
    print(email)
    getuserIdqueryfromemail="select userID from users WHERE email= '%s' "% (email)
    cursor.execute(getuserIdqueryfromemail)
    userID=cursor.fetchone()
    print(userID)
    return jsonify({'userID' : userID})

@app.route('/getuserIdsignup',methods=['GET'])
def getuserIdsignup():
    try:
        getuserIdquery='select userID from users ORDER BY userID DESC LIMIT 1;'
        cursor.execute(getuserIdquery)
        userID=cursor.fetchone()
        return jsonify({'userID' : userID})
    except:
        return jsonify({'userID': 10})

@app.route('/addtomylist',methods=['POST'])
def addtomylist():
    data = request.get_data()
    data = data.decode('utf-8')
    data = ast.literal_eval(data)
    userID=data[0]
    tmdbID=data[1]
    addtomylistquery= "INSERT INTO user_movielist values('%s', '%s')"% (userID, tmdbID)
    cursor.execute(addtomylistquery)
    db.commit()
    return ""

@app.route('/getmylist',methods=['GET'])
def getmylist():
    movieinfo=[]
    args = request.args
    userID = args['userId']
    if (userID!='0'):
        getuserIdquery='select tmdbID from user_movielist WHERE userID = %s;'% (userID)
        cursor.execute(getuserIdquery)
        movieIDs=cursor.fetchall()
        movieists=fetchmylist(movieIDs)
        return jsonify({'movieIDs' : movieists})
    else:
        return jsonify({'movieIDs': 0})

@app.route('/getcontentre',methods=['GET'])
def getcontentre():
    movieinfo=[]
    args = request.args
    userID = args['userId']
    if (userID!='0'):
        allrecommendations=[]
        getuserIdquery='select tmdbID from content_based_view WHERE userID = %s;'% (userID)
        cursor.execute(getuserIdquery)
        movieIDs=cursor.fetchall()
        movieists=contentrecommendations(movieIDs,userID)
        random.shuffle(movieists)
        allrecommendations.append(movieists)
        movieists = implicitcollaborativerecommendations(userID)
        random.shuffle(movieists)
        allrecommendations.append(movieists)
        movieists = explicitcollaborativerecommendations(userID)
        random.shuffle(movieists)
        allrecommendations.append(movieists)
        movieists = implicitneuralcollaborativerecommendations(userID)
        random.shuffle(movieists)
        allrecommendations.append(movieists)
        movieists = explicitneuralcollaborativerecommendations(userID)
        random.shuffle(movieists)
        allrecommendations.append(movieists)
        getuserIdquery = 'select tmdbID from user_movielist WHERE userID = %s;' % (userID)
        cursor.execute(getuserIdquery)
        movieIDs = cursor.fetchall()
        movieists = fetchmylist(movieIDs)
        allrecommendations.append(movieists)
        print(allrecommendations[3])
        print(allrecommendations[4])
        return jsonify({'content' : allrecommendations[0],'implicitcollaborative' : allrecommendations[1],'explicitcollaborative' : allrecommendations[2],'implicitneuralcollaborative' : allrecommendations[3],'explicitneuralcollaborative' : allrecommendations[4],'mylist' : allrecommendations[5]})
    else:
        return jsonify({'movieIDs': 0})

@app.route('/geticollre',methods=['GET'])
def geticollre():
    args = request.args
    userID = args['userId']
    if (userID!='0'):
        movieists=implicitcollaborativerecommendations(userID)
        random.shuffle(movieists)
        return jsonify({'movieIDs' : movieists})
    else:
        return jsonify({'movieIDs': 0})

@app.route('/getecollre',methods=['GET'])
def getecollre():
    args = request.args
    userID = args['userId']
    if (userID!='0'):
        movieists=explicitcollaborativerecommendations(userID)

        return jsonify({'movieIDs' : movieists})
    else:
        return jsonify({'movieIDs': 0})

@app.route('/getincollre',methods=['GET'])
def getincollre():
    args = request.args
    userID = args['userId']
    if (userID!='0'):
        movieists=implicitneuralcollaborativerecommendations(userID)

        return jsonify({'movieIDs' : movieists})
    else:
        return jsonify({'movieIDs': 0})

@app.route('/getencollre',methods=['GET'])
def getencollre():
    args = request.args
    userID = args['userId']
    if (userID!='0'):
        movieists=explicitneuralcollaborativerecommendations(userID)

        return jsonify({'movieIDs' : movieists})
    else:
        return jsonify({'movieIDs': 0})

@app.route('/gettrending',methods=['GET'])
def gettrending():
        gettmdbquery = 'SELECT tmdbid from (SELECT * FROM kryptonite.daily_update limit 8) as f'
        cursor.execute(gettmdbquery)
        movieIDs = cursor.fetchall()
        movieists = fetchmylist(movieIDs)
        return jsonify({'movieIDsfirst' : movieists[:4],'movieIDssecond' : movieists[4:]})

@app.route('/getmovies',methods=['GET'])
def getmovies():
        gettmdbquery = 'SELECT tmdbid from (SELECT * FROM kryptonite.daily_update limit 100) as v;'
        cursor.execute(gettmdbquery)
        movieIDs = cursor.fetchall()
        movieists = fetchmylist(movieIDs)
        return jsonify({'trending' : movieists[:20],'action' : movieists[20:40],'comedy' : movieists[40:60],'horror' : movieists[60:80],'romance' : movieists[80:90],'documentry' : movieists[90:104]})

@app.route('/ratingexplicit',methods=['POST'])
def ratingexplicit():
    data = request.get_data()
    data = data.decode('utf-8')
    data = ast.literal_eval(data)
    userID=data[0]
    tmdbID=data[1]
    rating=data[2]
    print(userID, tmdbID, rating)
    addtomylistquery= "INSERT INTO rating_explicit values(%s, %s,%s,SYSDATE())"% (int(userID), int(tmdbID),int(rating))
    cursor.execute(addtomylistquery)
    db.commit()
    return ""


@app.route('/ratingimplicit',methods=['POST'])
def ratingimplicit():
    data = request.get_data()
    data = data.decode('utf-8')
    data = ast.literal_eval(data)
    userID=data[0]
    tmdbID=data[1]
    interaction=1
    print(userID,tmdbID,interaction)
    addtomylistquery= "INSERT INTO rating_implicit values(%s,%s,%s,SYSDATE())"% (int(userID), int(tmdbID),int(interaction))
    cursor.execute(addtomylistquery)
    db.commit()
    return ""










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



if __name__ == "__main__":
    app.run(debug=True)