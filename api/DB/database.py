"""This file contains the methods to interact with the database."""

import hmac
import hashlib
import random
import datetime
import string
import json
from sqlalchemy.sql import text
import bcrypt
from flask import request, Blueprint
from extensions import da
from mail.mail import sendVerifyLink, sendNewPassword

datab = Blueprint(name="datab", import_name=__name__)
pepper = json.load(open("config.json"))


class SqlFunctions:
    """This class contains methods to interact with the database with SQL queries."""

    def __init__(self, database):
        self.database = database

    def select(self, fields, table, condition):
        """This method selects data from the database."""
        query = text(f"SELECT {fields} FROM connecte.{table} WHERE {condition}")
        return self.database.session.execute(query)

    def insert(self, table, values):
        """This method inserts data into the database."""
        columns = ", ".join(values.keys())
        vals = ", ".join([f"'{v}'" for v in values.values()])
        query = text(f"INSERT INTO connecte.{table} ({columns}) VALUES({vals})")
        self.database.session.execute(query)
        self.database.session.commit()

    def update(self, table, setValues, condition):
        """This method updates data in the database."""
        setClause = ", ".join(
            [f"{key} = '{value}'" for key, value in setValues.items()]
        )
        query = text(f"UPDATE connecte.{table} SET {setClause} WHERE {condition}")
        self.database.session.execute(query)
        self.database.session.commit()


sql_functions = SqlFunctions(da)


class Players(da.Model):
    """This class represents the PLAYERS table in the database."""

    __tablename__ = "connecte.PLAYERS"
    username = da.Column(da.String(50), primary_key=True)
    token = da.Column(da.String(255))
    hashed_pass = da.Column(da.String(255))
    email = da.Column(da.String(255))
    verified = da.Column(da.Integer)


class Games(da.Model):
    """This class represents the GAMES table in the database."""

    __tablename__ = "connecte.GAMES"
    id = da.Column(da.Integer, primary_key=True, autoincrement=True)
    game_board = da.Column(da.String(1024))
    time_date = da.Column(da.DateTime, default=datetime.datetime.now())


class PlayersGames(da.Model):
    """This class represents the PLAYERS_GAMES table in the database."""

    __tablename__ = "connecte.PLAYERS_GAMES"
    id = da.Column(da.Integer, primary_key=True, autoincrement=True)
    FKplayer = da.Column(da.String(50), da.ForeignKey("players.username"))
    FKgame = da.Column(da.Integer, da.ForeignKey("games.id"))
    WDL = da.Column(da.String(1))
    which_turn = da.Column(da.Integer)


def generateId(lenght, prefix=""):
    """This method generates a random ID with with a specific length."""
    return prefix.join(random.choices(string.ascii_lowercase + string.digits, k=lenght))


@datab.route("/verify", methods=["POST"])
def verify():
    """This method verifies the users email by checking the verification ID in the request.
    If verification ID is valid, the user is verified and the verification ID is removed
    from the database.
    If not, an error message is sent to the client."""
    try:
        data = request.get_json()
        id = data["id"]
        user = sql_functions.select(
            "username, hashed_pass, email, token", "PLAYERS", f"verifyID = '{id}'"
        ).first()
        if user is None:
            return {"message": "404 verification link invalid or expired"}
        sql_functions.update("PLAYERS", {"verified": 1}, f"verifyID = '{id}'")
        sql_functions.update("PLAYERS", {"verifyID": ""}, f"verifyID = '{id}'")
        return {"message": f"Thank you for verifying your email {user.username} !"}

    except Exception as e:
        return {"message": str(e)}


@datab.route("/registerPlayer", methods=["POST"])
def createPlayer():
    """This method creates a new player in the database."""
    try:
        data = request.get_json()
        usern = data["username"]
        passw = data["hashed_pass"]
        mail = data["email"]

        if len(usern) < 5:
            return {"message": "Username must be at least 5 characters long"}
        if len(passw) < 8:
            return {"message": "Password must be at least 8 characters long"}
        if usern.find(" ") != -1:
            return {"message": "Username cannot contain spaces"}
        if mail.find("@") == -1:
            return {"message": "Invalid email"}

        taken = sql_functions.select(
            "username, hashed_pass, email, token", "PLAYERS", f"username = '{usern}'"
        ).first()

        if taken is not None:
            return {"message": "Username already taken"}

        existingVerifyID = "notNone"
        while existingVerifyID is not None:
            verifyID = generateId(50)
            existingVerifyID = sql_functions.select(
                "verifyID", "PLAYERS", f"verifyID = '{verifyID}'"
            ).first()

        sendVerifyLink(mail, verifyID, usern)

        passw = hmac.new(
            pepper["Pepper"].encode("utf-8"), passw.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        salt = bcrypt.gensalt()
        passw = bcrypt.hashpw(passw.encode("utf-8"), salt)
        passw = passw.decode("utf-8")
        sql_functions.insert(
            "PLAYERS",
            {
                "username": usern,
                "hashed_pass": passw,
                "email": mail,
                "token": "",
                "verifyID": verifyID,
            },
        )

        return {"message": "Added to database"}
    except Exception as e:
        return {"message": str(e)}


def checkToken(token):
    """This method checks if the token is valid and returns the user's data."""
    if token is not None:
        return sql_functions.select(
            "username, hashed_pass, email, token", "PLAYERS", f"token = '{token}'"
        ).first()
    return None


def getName(token):
    """This method returns the username of the user with the specified token."""
    if token is not None:
        return sql_functions.select(
            "username, hashed_pass, email, token", "PLAYERS", f"token = '{token}'"
        ).first()
    return "Guest"


def registerGame(gameBoard, players, winner):
    """This method registers a game and its data into the database."""
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    sql_functions.insert("GAMES", {"game_board": gameBoard, "time_date": time})
    game = sql_functions.select("*", "GAMES", f"time_date = '{time}'").first()

    da.session.commit()

    draw = False

    if winner is None:
        draw = True
        winner = {
            "color": -1,
            "requestID": -1,
            "cookie": -1,
            "token": -1,
        }

    for player in players:
        if winner["cookie"] == player["cookie"] and winner["color"] == player["color"]:
            wdl = "W"
        elif draw:
            wdl = "D"
        else:
            wdl = "L"

        if player["token"] != -1:
            pl = (
                sql_functions.select(
                    "username, hashed_pass, email, token",
                    "PLAYERS",
                    f"token = '{player['token']}'",
                )
                .first()
                .username
            )
        else:
            pl = "Guest"

        sql_functions.insert(
            "PLAYERS_GAMES",
            {
                "FKplayer": pl,
                "FKgame": game.id,
                "WDL": wdl,
                "which_turn": player["color"],
            },
        )
    return {"message": f"Added game to database", "gameId": game.id}


def userExists(usern):
    """This method checks if the user exists in the database.
    Returns user data if user exists, otherwise returns None."""
    user = Players.query.filter_by(username=usern).first()
    return user


@datab.route("/stats", methods=["POST"])
def getuserData():
    """This method returns the user's data and game history by checking
    the token in the request and returning the user's data."""
    data = request.get_json()
    if data["token"] is None or checkToken(data["token"]) is None:
        return {"error": "Authentication failure"}
    user = checkToken(data["token"])
    username = user.username
    email = user.email
    winCount = len(
        sql_functions.select(
            "*", "PLAYERS_GAMES", f"FKplayer = '{username}' AND WDL ='W'"
        ).all()
    )
    drawCount = len(
        sql_functions.select(
            "*", "PLAYERS_GAMES", f"FKplayer = '{username}' AND WDL ='D'"
        ).all()
    )
    loseCount = len(
        sql_functions.select(
            "*", "PLAYERS_GAMES", f"FKplayer = '{username}' AND WDL ='L'"
        ).all()
    )
    playerGames = sql_functions.select(
        "*", "PLAYERS_GAMES", f"FKplayer = '{username}'"
    ).all()

    games = []

    for game in playerGames:
        board = (
            sql_functions.select("game_board", "GAMES", f"id = {game.FKgame}")
            .first()
            .game_board
        )
        time = (
            sql_functions.select("time_date", "GAMES", f"id = {game.FKgame}")
            .first()
            .time_date.strftime("%Y-%m-%d %H:%M:%S")
        )
        opponentsIDs = sql_functions.select(
            "FKplayer",
            "PLAYERS_GAMES",
            f"FKgame = {game.FKgame} AND FKplayer != '{username}'",
        ).all()
        selfCount = len(
            sql_functions.select(
                "FKplayer",
                "PLAYERS_GAMES",
                f"FKgame = {game.FKgame} AND FKplayer = '{username}'",
            ).all()
        )
        opponents = ""
        if selfCount > 1:
            opponents = "You " * (
                selfCount - 1
            )  # If the player played against themselves
        for opponent in opponentsIDs:
            opp = opponent.FKplayer
            opponents += opp + " "
        games.append(
            {
                "gameId": game.FKgame,
                "WDL": game.WDL,
                "which_turn": game.which_turn,
                "board": board,
                "time": time,
                "opponents": opponents,
            }
        )

    data = {
        "username": username,
        "email": email,
        "winCount": winCount,
        "drawCount": drawCount,
        "loseCount": loseCount,
        "games": games,
    }
    return {"message": data}


@datab.route("/checkUser", methods=["POST"])
def checkUser():
    """This method checks if the user exists in the database by checking
    the username and password in the request."""
    try:
        data = request.get_json()
        usern = data["username"]
        passw = data["hashed_pass"]

        user = sql_functions.select(
            "username, hashed_pass, email, token", "PLAYERS", f"username = '{usern}'"
        ).first()
        if user is None:
            return {"message": "User not found or Incorrect password"}
        if not bcrypt.checkpw(
            hmac.new(
                pepper["Pepper"].encode("utf-8"), passw.encode("utf-8"), hashlib.sha256
            )
            .hexdigest()
            .encode("utf-8"),
            str.encode(user.hashed_pass, "utf-8"),
        ):
            return {"message": "User not found or Incorrect password"}
        token = generateId(255)
        sql_functions.update("PLAYERS", {"token": token}, f"username = '{usern}'")
        return {"token": token}
    except Exception as e:
        return {"message": str(e)}


@datab.route("/resetPassword", methods=["POST"])
def resetPass():
    """This method finds username specified in the request,
    checks if that user is verified.
    If user is verified, a new password is sent to their email.
    If not, an error message is sent to the client"""
    try:
        data = request.get_json()
        username = data["username"]

        user = sql_functions.select(
            "email, verified, username", "PLAYERS", f"username = '{username}'"
        ).first()

        if user is None:
            return {"error": "Username doesn't exist"}
        if user.verified == 0:
            return {"error": "User needs to be verified to reset password"}

        newPassword = generateId(10)

        passw = hmac.new(
            pepper["Pepper"].encode("utf-8"),
            newPassword.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        salt = bcrypt.gensalt()
        passw = bcrypt.hashpw(passw.encode("utf-8"), salt)
        passw = passw.decode("utf-8")

        sql_functions.update(
            "PLAYERS", {"hashed_pass": passw}, f"username = '{user.username}'"
        )
        sendNewPassword(user.email, newPassword, user.username)

        return {"message": "Password reset email sent"}

    except Exception as e:
        return {"error": str(e)}
