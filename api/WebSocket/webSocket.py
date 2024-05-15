"""This module is responsible for handling the WebSocket connections and requests for the game"""

from threading import Thread
import time
from flask import Blueprint, request, copy_current_request_context
from flask_socketio import emit, join_room, leave_room, rooms
from Connect4.connect4 import Connect4
from extensions import cors, socketio
from DB.database import registerGame, generateId, checkToken, registerLeave
from Bot.Connect import connectBotToGame


games = {}

room = Blueprint(name="room", import_name=__name__)


@room.route("/getRoom", methods=["POST"], strict_slashes=False)
def getRoom():
    # for future, data['w'] is width and data['h'] is heigth
    """This method is responsible for creating a new game room"""
    data = request.get_json()
    gameId = generateId(8)

    if 1 > data["mode"] or data["mode"] > 3 or data["mode"] is None:
        data["mode"] = 1
    if 2 > data["w"] or data["w"] > 15 or data["w"] is None:
        data["w"] = 7
    if 2 > data["h"] or data["h"] > 15 or data["h"] is None:
        data["h"] = 6
    if 2 > data["playerCount"] or data["playerCount"] > 4 or data["playerCount"] is None:
        data["playerCount"] = 2
    if 2 > data["winCondition"] or data["winCondition"] is None:
        data["winCondition"] = 4

    if data["mode"] != 3:
        games[gameId] = [time.time(), Connect4(gameMode=data["mode"], w=data["w"], h=data["h"], playerCount=data["playerCount"],
                                               k=data["winCondition"])]

    elif data["mode"] == 3:
        game = Connect4()
        difficulty = 2
        if(data["botDifficulty"] == 1):
            difficulty = 2
        if(data["botDifficulty"] == 2):
            difficulty = 4
        if(data["botDifficulty"] == 3):
            difficulty = 6
        if(data["botDifficulty"] == 4):
            difficulty = 7
        print(difficulty)
        games[gameId] = [time.time(), game]
        connectBotToGame(gameId, difficulty)
    return {"gameId": gameId}


@socketio.on("join")
def handleJoin(data):
    """This method is responsible for handling the join event for the game room"""
    if "gameId" not in data or "id" not in data or "token" not in data:
        emit("error", {"state": "no_room_found"})
        return
    gameId = data["gameId"]
    if gameId in games:
        if games[gameId][1].state == 1:
            for player in games[gameId][1].players:
                if data["id"] == player["cookie"]:
                    join_room(gameId)
                    player["requestID"] = request.sid

                    emit(
                        "message",
                        {
                            "state": "playing_game",
                            "board": games[gameId][1].getBoardString(),
                            "move": False,
                            "color": games[gameId][1].toMove["color"],
                            "name": games[gameId][1].toMove["username"],
                            "name": games[gameId][1].toMove["username"],
                        },
                        room=gameId,
                    )
                    emit(
                        "message",
                        {
                            "state": "playing_game",
                            "board": games[gameId][1].getBoardString(),
                            "move": True,
                            "color": games[gameId][1].toMove["color"],
                            "name": games[gameId][1].toMove["username"],
                        },
                        room=games[gameId][1].toMove["requestID"],
                    )
                    return

            join_room(gameId)
            emit(
                "message",
                {
                    "state": "playing_game",
                    "board": games[gameId][1].getBoardString(),
                    "move": False,
                    "color": games[gameId][1].toMove["color"],
                    "name": games[gameId][1].toMove["username"],
                    "spectator": True,
                },
                room=request.sid,
            )

            return
        if data["id"] is None:
            id = generateId(15)
        else:
            id = data["id"]

        player = checkToken(data["token"])
        if player is not None:
            token = data["token"]
            name = player[0]
        else:
            token = -1
            name = "Guest"

        games[gameId][1].addPlayer(request.sid, id, token, name)
        games[gameId][0] = time.time()
        emit("cookie", {"id": id}, room=request.sid)
        join_room(gameId)
        emit("message", {"state": "waiting_for_one_player"})
        if games[gameId][1].state == 1:
            emit(
                "message",
                {
                    "state": "playing_game",
                    "board": games[gameId][1].getBoardString(),
                    "move": False,
                    "color": games[gameId][1].toMove["color"],
                    "name": games[gameId][1].toMove["username"],
                },
                room=gameId,
            )
            emit(
                "message",
                {
                    "state": "playing_game",
                    "board": games[gameId][1].getBoardString(),
                    "move": True,
                    "color": games[gameId][1].toMove["color"],
                    "name": games[gameId][1].toMove["username"],
                },
                room=games[gameId][1].toMove["requestID"],
            )

        return
    emit("error", {"state": "no_room_found"})


@socketio.on("move")
def handleMove(data):
    """This method is responsible for handling the move event for the game room"""
    try:
        gameId = data["gameId"]
        game = games[gameId][1]
        move = int(data["move"])
        game.placeTile(move)

    except:
        emit(
            "message",
            {
                "state": "playing_game",
                "board": games[gameId][1].getBoardString(),
                "move": True,
                "error": "Row already full",
                "color": games[gameId][1].toMove["color"],
                "name": games[gameId][1].toMove["username"],
            },
            room=request.sid,
        )

        return

    if game.checkForWin():
        game.changeMode()

        data = registerGame(
            game.getBoardString(), game.players, game.toMove, game.k
        )
        emit(
            "message",
            {
                "state": "game_end",
                "board": games[gameId][1].getBoardString(),
                "move": False,
                "winner": False,
                "draw": False,
                "name": games[gameId][1].toMove["username"],
            },
            room=gameId,
        )
        emit(
            "message",
            {
                "state": "game_end",
                "board": games[gameId][1].getBoardString(),
                "move": False,
                "winner": True,
                "draw": False,
                "name": games[gameId][1].toMove["username"],
            },
            room=games[gameId][1].toMove["requestID"],
        )
        game.printMode()

        game.changeState()
        game.printMode()
        return

    if game.checkForDraw():
        game.changeMode()
        data = registerGame(game.getBoardString(), games[gameId][1].players, None, game.k)
        emit(
            "message",
            {
                "state": "game_end",
                "board": games[gameId][1].getBoardString(),
                "move": False,
                "winner": False,
                "draw": True,
            },
            room=gameId,
        )
        game.changeState()
        return

    game.changeToMove()
    emit(
        "message",
        {
            "state": "playing_game",
            "board": games[gameId][1].getBoardString(),
            "move": False,
            "color": games[gameId][1].toMove["color"],
            "name": games[gameId][1].toMove["username"],
        },
        room=gameId,
    )
    emit(
        "message",
        {
            "state": "playing_game",
            "board": games[gameId][1].getBoardString(),
            "move": True,
            "color": games[gameId][1].toMove["color"],
            "name": games[gameId][1].toMove["username"],
        },
        room=games[gameId][1].toMove["requestID"],
    )

    return


@socketio.on("disconnect")
def handleLeave():
    """This method is responsible for handling the disconnect event for the game room"""

    @copy_current_request_context
    def abandonGame(userRoom, id):
        samebrowser = True
        firstid = (
            games[userRoom][1].players[0]["cookie"]
        )  # if something breaks this will DEFINETELY be the culprit
        for player in games[userRoom][1].players:

            if player["cookie"] != firstid:
                samebrowser = False  # Should be removed in the future

        if samebrowser is False:
            time.sleep(15)
        game = games[userRoom][1]
        for player in game.players:
            if player["requestID"] == id:
                data = registerLeave(game.getBoardString(), game.players, player)
                emit(
                    "message",
                    {
                        "state": "game_end",
                        "board": games[userRoom][1].getBoardString(),
                        "move": False,
                        "winner": True,
                        "draw": False,
                        "error": "opponent disconnected",
                    },
                    room=userRoom,
                )
                games[userRoom][1].changeState()

    userRoom = rooms(request.sid)[0]
    if len(userRoom) != 8:
        userRoom = rooms(request.sid)[1]

    if userRoom not in games:
        return

    for player in games[userRoom][1].players:
        if player["requestID"] == request.sid:
            thread = Thread(target=abandonGame, args=(userRoom, request.sid))
            thread.start()

    games[userRoom][1].changeMode()
    leave_room(userRoom)
