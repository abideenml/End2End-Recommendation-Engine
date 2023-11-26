import ast
from flask import Flask, request, jsonify
from flask_cors import CORS
import random
from . import config
from . import database

DATABASE_USERNAME = config.DATABASE_USERNAME
DATABASE_PASSWORD = config.DATABASE_PASSWORD
DATABASE_HOST = config.DATABASE_HOST
DATABASE_NAME = config.DATABASE_NAME
API_key = config.TMDB_API_KEY
cursor, db = database.get_db()



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


if __name__ == "__main__":
    app.run(debug=True)