
# from WebSocket.webSocket import app
from flask import Flask, Response, request, Blueprint
from extensions import da
from sqlalchemy.sql import text
import json
import bcrypt
import hmac
import hashlib
import random
import datetime
import string
import datetime

datab = Blueprint(name="datab", import_name=__name__)
pepper = json.load(open("config.json"))

class sqlFunctions:
    def __init__(self, database):
        self.database = database

    def select(self, fields, table, condition):
        query = text(f"SELECT {fields} FROM connecte.{table} WHERE {condition}")
        return self.database.session.execute(query)


    def insert(self, table, values):
        columns = ', '.join(values.keys())
        vals = ', '.join([f"'{v}'" for v in values.values()])
        query = text(f"INSERT INTO connecte.{table} ({columns}) VALUES({vals})")
        self.database.session.execute(query)
        self.database.session.commit()


    def update(self, table, set_values, condition):
        set_clause = ', '.join([f"{key} = '{value}'" for key, value in set_values.items()])
        query = text(f"UPDATE connecte.{table} SET {set_clause} WHERE {condition}")
        self.database.session.execute(query)
        self.database.session.commit()


sql_functions = sqlFunctions(da)
class PLAYERS(da.Model):
    __tablename__ = 'connecte.PLAYERS'
    username = da.Column(da.String(50), primary_key=True)
    token = da.Column(da.String(255))
    hashed_pass = da.Column(da.String(255))
    email = da.Column(da.String(255))


class GAMES(da.Model):
    id = da.Column(da.Integer, primary_key=True, autoincrement=True)
    game_board = da.Column(da.String(1024))
    time_date = da.Column(da.DateTime, default=datetime.datetime.now())


class PLAYERS_GAMES(da.Model):
    id = da.Column(da.Integer, primary_key=True, autoincrement=True)
    FKplayer = da.Column(da.String(50), da.ForeignKey('players.username'))
    FKgame = da.Column(da.Integer, da.ForeignKey('games.id'))
    WDL = da.Column(da.String(1))
    which_turn = da.Column(da.Integer)


def generateId(lenght, prefix=""):
    return prefix.join(random.choices(string.ascii_lowercase + string.digits, k=lenght))


@datab.route('/registerPlayer', methods=['POST'])
def createPlayer():
    try:
        data = request.get_json()
        usern = data['username']
        passw = data['hashed_pass']
        mail = data['email']

        if len(usern) < 5:
            return {'message': 'Username must be at least 5 characters long'}
        if len(passw) < 8:
            return {'message': 'Password must be at least 8 characters long'}

        # Validate if it is a valid email later

        taken = sql_functions.select("username, hashed_pass, email, token", "PLAYERS", f"username = '{usern}'").first()

        if (taken is not None):
            return {'message': 'Username already taken'}

        passw = hmac.new(pepper["Pepper"].encode('utf-8'), passw.encode('utf-8'), hashlib.sha256).hexdigest()
        salt = bcrypt.gensalt()
        passw = bcrypt.hashpw(passw.encode('utf-8'), salt)
        passw = passw.decode("utf-8")
        sql_functions.insert("PLAYERS", {"username": usern, "hashed_pass": passw, "email": mail, "token": ""})

        return {'message': 'Added to database'}
    except Exception as e:
        return {'message': str(e)}


def checkToken(token):
    if token is not None:
        return sql_functions.select("username, hashed_pass, email, token", "PLAYERS", f"token = '{token}'").first()
    return None

def getName(token):
    if token is not None:
        return sql_functions.select("username, hashed_pass, email, token", "PLAYERS", f"token = '{token}'").first()
    return "Guest"

def registerGame(gameBoard, players, winner):
    now = datetime.datetime.utcnow()
    time = now.strftime('%Y-%m-%d %H:%M:%S')
    sql_functions.insert("GAMES", {"game_board": gameBoard, "time_date": time})
    game = sql_functions.select("*", "GAMES", f"time_date = '{time}'").first()

    da.session.commit()

    draw = False

    if winner == None:
        draw = True
        winner = [-1, -1, -1, -1]

    for player in players:
        if (winner[2] == player[2]):
            wdl = 'W'
        elif (draw):
            wdl = 'D'
        else:
            wdl = 'L'

        if player[3] != -1:
            pl = sql_functions.select("username, hashed_pass, email, token", "PLAYERS", f"token = '{player[3]}'").first().username
        else:
            pl = "Guest"

        sql_functions.insert("PLAYERS_GAMES", {"FKplayer": pl, "FKgame": game.id, "WDL": wdl, "which_turn": player[0]})

    return {'message': f'Added game to database', 'gameId': game.id}


def userExists(usern):
    user = PLAYERS.query.filter_by(username=usern).first()
    return user


@datab.route('/stats', methods=['POST'])
def getuserData():
    data = request.get_json()
    if data['token'] == None or checkToken(data['token']) == None:
        return {'error': "Authentication failure"}
    user = checkToken(data['token'])
    username = user.username
    email = user.email
    winCount = len(sql_functions.select("*", "PLAYERS_GAMES", f"FKplayer = '{username}' AND WDL ='W'").all())
    drawCount = len(sql_functions.select("*", "PLAYERS_GAMES", f"FKplayer = '{username}' AND WDL ='D'").all())
    loseCount = len(sql_functions.select("*", "PLAYERS_GAMES", f"FKplayer = '{username}' AND WDL ='L'").all())
    data = {'username': username, 'email': email, 'winCount': winCount, 'drawCount': drawCount, 'loseCount': loseCount}
    return {'message': data}


@datab.route('/checkUser', methods=['POST'])
def checkUser():
    try:
        data = request.get_json()
        usern = data['username']
        passw = data['hashed_pass']

        user = result = sql_functions.select("username, hashed_pass, email, token", "PLAYERS", f"username = '{usern}'").first()
        if user is None:
            return {'message': 'User not found or Incorrect password'}
        if not bcrypt.checkpw(
                hmac.new(pepper["Pepper"].encode('utf-8'), passw.encode('utf-8'), hashlib.sha256).hexdigest().encode(
                        'utf-8'), str.encode(user.hashed_pass, 'utf-8')):
            return {'message': 'User not found or Incorrect password'}
        token = generateId(255)
        sql_functions.update("PLAYERS", {"token": token}, f"username = '{usern}'")
        return {'token': token}
    except Exception as e:
        return {'message': str(e)}

