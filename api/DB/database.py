from flask_sqlalchemy import SQLAlchemy
# from WebSocket.webSocket import app
from flask import Flask, Response, request, Blueprint
from extensions import da
import json
import bcrypt
import hmac
import hashlib

import datetime

datab = Blueprint(name="datab", import_name=__name__)
pepper = json.load(open("config.json"))


class PLAYERS(da.Model):
    username = da.Column(da.String(50), primary_key=True)
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

        pl = PLAYERS(username=usern, hashed_pass=passw, email=mail)
        da.session.add(pl)
        da.session.commit()

        return {'message': f'Added {usern} to database'}
    except Exception as e:
        return {'message': str(e)}


def createGuestPlayer(id):
    pl = PLAYERS(username=id, hashed_pass="", email="")
    da.session.add(pl)
    da.session.commit()

    return {'message': f'Added {id} to database'}


def registerGame(gameBoard, players, winner):
    print("called")
    try:
        game = GAMES(game_board=gameBoard)
        da.session.add(game)
        da.session.commit()

        for player in players:
            if (winner == player[1]):
                wdl = 'W'
            elif (winner == None):
                wdl = 'D'
            else:
                wdl = 'L'
            pg = PLAYERS_GAMES(FKplayer=player[2], FKgame=game.id, WDL=wdl, which_turn=player[0])
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
        if not user:
            return {'message': 'User not found'}
        if not bcrypt.checkpw(hmac.new(pepper["Pepper"].encode('utf-8'), passw.encode('utf-8'), hashlib.sha256).hexdigest().encode('utf-8'), user.hashed_pass):
            return {'message': 'Incorrect password'}
        return {'message': 'Success'}
    except Exception as e:
        return {'message': str(e)}


@datab.route('/addPlayerGame', methods=['GET'])
def addPlayerGame():
    try:
        data = request.get_json()
        player = data['player']
        game = data['game']
        WDL = data['WDL']
        turn = data['turn']

        pg = PLAYERS_GAMES(FKplayer=player, FKgame=game, WDL=WDL, which_turn=turn)
        da.session.add(pg)
        da.session.commit()

        return {'message': 'Added player to game'}
    except Exception as e:
        return {'message': str(e)}
