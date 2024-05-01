"""This module is responsible for handling the WebSocket connections and requests for the game"""

from threading import Thread
import time
from flask import Blueprint, request, copy_current_request_context
from flask_socketio import emit, join_room, leave_room, rooms
from Connect4.connect4 import Connect4
from extensions import cors, socketio
from DB.database import registerGame, generateId, checkToken, getName
from Bot.Connect import connectBotToGame



games = {}

room = Blueprint(name="room", import_name=__name__)


@room.route("/getRoom", methods=["POST"], strict_slashes=False)
def getRoom():
    # for future, data['w'] is width and data['h'] is heigth
    """This method is responsible for creating a new game room"""
    data = request.get_json()
    gameId = generateId(8)
    if data['mode'] == 2:
        games[gameId] = [time.time(),Connect4(gameMode=2)]
    elif data['mode'] == 3:
        game = Connect4()
        games[gameId] = [time.time(),game]
        connectBotToGame(gameId,7)
    elif data['winCondition'] >=1:
        games[gameId] = [time.time(),Connect4(k=data['winCondition'],playerCount=data['playerCount'])]
    else:
        games[gameId] = [time.time(),Connect4(playerCount=data['playerCount'])]


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
            for x in games[gameId][1].players:
                if data["id"] == x[2]:
                    join_room(gameId)
                    x[1] = request.sid

                    emit('message',{'state':'playing_game','board':games[gameId][1].getBoardString(), 'move':False, 'color':games[gameId][1].toMove["color"], 'name':games[gameId][1].toMove["username"], 'name':games[gameId][1].toMove["username"]}, room=gameId)
                    emit('message',{'state':'playing_game','board':games[gameId][1].getBoardString(), 'move':True, 'color':games[gameId][1].toMove["color"], 'name':games[gameId][1].toMove["username"]}, room=games[gameId][1].toMove["requestID"])
                    return

            join_room(gameId)
            emit('message',{'state':'playing_game','board':games[gameId][1].getBoardString(), 'move':False, 'color':games[gameId][1].toMove["color"], 'name':games[gameId][1].toMove["username"], 'spectator':True }, room=request.sid)

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
        emit('message',{'state':'waiting_for_one_player'})
        if(games[gameId][1].state == 1):
            emit('message',{'state':'playing_game','board':games[gameId][1].getBoardString(), 'move':False, 'color':games[gameId][1].toMove["color"], 'name':games[gameId][1].toMove["username"]}, room=gameId)
            emit('message',{'state':'playing_game','board':games[gameId][1].getBoardString(), 'move':True, 'color':games[gameId][1].toMove["color"], 'name':games[gameId][1].toMove["username"]}, room=games[gameId][1].toMove["requestID"])

        return
    emit("error", {"state": "no_room_found"})


@socketio.on("move")
def handleMove(data):
    '''This method is responsible for handling the move event for the game room'''
    try:
        gameId = data["gameId"]
        game = games[gameId][1]
        move = int(data["move"])
        game.placeTile(move)

    except:
        emit('message',{'state':'playing_game','board':games[gameId][1].getBoardString(), 'move':True, 'error':'Row already full', 'color':games[gameId][1].toMove["color"], 'name':games[gameId][1].toMove["username"]}, room=request.sid)

        return

    if game.checkForWin():
        game.changeMode()

        data = registerGame(game.getBoardString(), games[gameId][1].players, games[gameId][1].toMove)
        emit('message',{'state':'game_end','board':games[gameId][1].getBoardString(), 'move':False, 'winner':False , 'draw':False, 'name':games[gameId][1].toMove["username"]}, room=gameId)
        emit('message',{'state':'game_end','board':games[gameId][1].getBoardString(), 'move':False, 'winner':True , 'draw':False, 'name':games[gameId][1].toMove["username"]}, room=games[gameId][1].toMove["requestID"])
        game.printMode()

        game.changeState()
        game.printMode()
        return

    if game.checkForDraw():
        game.changeMode()
        data = registerGame(game.getBoardString(), games[gameId][1].players, None)
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
    emit('message',{'state':'playing_game','board':games[gameId][1].getBoardString(), 'move':False, 'color':games[gameId][1].toMove["color"], 'name':games[gameId][1].toMove["username"]}, room=gameId)
    emit('message',{'state':'playing_game','board':games[gameId][1].getBoardString(), 'move':True, 'color':games[gameId][1].toMove["color"], 'name':games[gameId][1].toMove["username"]}, room=games[gameId][1].toMove["requestID"])


    return


@socketio.on("disconnect")
def handleLeave():
    '''This method is responsible for handling the disconnect event for the game room'''
    @copy_current_request_context
    def abandonGame(userRoom, id):
        samebrowser = True
        firstid = games[userRoom][1].players[0][2] # if something breaks this will be the culprit
        for x in games[userRoom][1].players:

            if x[2] != firstid:
                samebrowser = False

        if samebrowser is False:
            time.sleep(15)
        for x in games[userRoom][1].players:
            if x[1] == id:
                data = registerGame(
                    games[userRoom][1].getBoardString(), games[userRoom][1].players, x
                )
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

    for x in games[userRoom][1].players:
        if x[1] == request.sid:
            thread = Thread(target=abandonGame, args=(userRoom, request.sid))
            thread.start()

    games[userRoom][1].changeMode()
    leave_room(userRoom)
