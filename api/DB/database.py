from flask_sqlalchemy import SQLAlchemy
# from WebSocket.webSocket import app
from flask import Flask, Response, request, Blueprint
from extensions import da
import json
import bcrypt
import hmac
import hashlib
import random
import datetime
import string

datab = Blueprint(name="datab", import_name=__name__)
pepper = json.load(open("config.json"))


class PLAYERS(da.Model):
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

        taken = PLAYERS.query.filter_by(username=usern).first()
        if (taken):
            return {'message': 'Username already taken'}

        passw = hmac.new(pepper["Pepper"].encode('utf-8'), passw.encode('utf-8'), hashlib.sha256).hexdigest()
        salt = bcrypt.gensalt()
        passw = bcrypt.hashpw(passw.encode('utf-8'), salt)

        pl = PLAYERS(username=usern, hashed_pass=passw, email=mail, token = "")
        da.session.add(pl)
        da.session.commit()

        return {'message': f'Added {usern} to database'}
    except Exception as e:
        return {'message': str(e)}
    

def checkToken(token):
    if token != "" or token != None:
        return PLAYERS.query.filter_by(token=token).first()
    return None


def registerGame(gameBoard, players, winner):
    print("called")
    try:
        game = GAMES(game_board=gameBoard)
        da.session.add(game)
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
                pl = PLAYERS.query.filter_by(token=player[3]).first().username
            else:
                pl = "Guest"

                
            pg = PLAYERS_GAMES(FKplayer=pl, FKgame=game.id, WDL=wdl, which_turn=player[0])
            da.session.add(pg)
            da.session.commit()

        return {'message': f'Added game to database', 'gameId': game.id}
    except Exception as e:
        return {'message': str(e)}


def userExists(usern):
    user = PLAYERS.query.filter_by(username=usern).first()

    return user


@datab.route('/checkUser', methods=['POST'])
def checkUser():
    try:
        data = request.get_json()
        usern = data['username']
        passw = data['hashed_pass']
        
        user = PLAYERS.query.filter_by(username=usern).first()
        
        print(type(passw))
        if not user:
            return {'message': 'User not found or Incorrect password'}
        if not bcrypt.checkpw(hmac.new(pepper["Pepper"].encode('utf-8'), passw.encode('utf-8'), hashlib.sha256).hexdigest().encode('utf-8'), str.encode(user.hashed_pass, 'utf-8')):
            return {'message': 'User not found or Incorrect password'}
        token = generateId(255)
        user.token = token
        da.session.commit()
        return {'token' : token}
    except Exception as e:
        return {'message': str(e)}
