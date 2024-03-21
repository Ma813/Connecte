from flask import Flask, Blueprint, render_template, request, copy_current_request_context
from flask_socketio import emit, join_room, leave_room, rooms
from threading import Thread
import random
import time
from Connect4.connect4 import Connect4
from extensions import cors, socketio
from DB.database import registerGame, createGuestPlayer, userExists



games = {}

room = Blueprint(name="room", import_name=__name__)

@room.route("/getRoom", methods=["GET"], strict_slashes=False)
def getRoom():
    gameId = generateId(8)
    games[gameId] = [time.time(),Connect4()]

    return {'gameId':gameId}



def generateId(lenght, prefix=""):
    characters = "qwertyuiopasdfghjklzxcvbnm123456789"
    return prefix.join(random.sample(characters,lenght))
    

@socketio.on('join')
def handleJoin(data): 
    if 'gameId' not in data:
        return
    gameId = data['gameId']
    if gameId in games:
        if(games[gameId][1].state == 1):
            for x in games[gameId][1].players:
                if(data['id'] == x[2]):
                    join_room(gameId)
                    x[1] = request.sid
                    emit('message',{'state':'playing_game','board':games[gameId][1].getBoardString(), 'move':False, 'color':games[gameId][1].toMove[0]}, room=gameId)
                    emit('message',{'state':'playing_game','board':games[gameId][1].getBoardString(), 'move':True, 'color':games[gameId][1].toMove[0]}, room=games[gameId][1].toMove[1])
                    return

            join_room(gameId)
            emit('message',{'state':'playing_game','board':games[gameId][1].getBoardString(), 'move':False, 'color':games[gameId][1].toMove[0] }, room=gameId)
            return
        print(data['id'])
        if(data['id'] == None):
            id = generateId(15)
        else:
            id = data['id']


        # if data['username'] == None and data['id'] == None:
            

        
        
        games[gameId][1].addPlayer(request.sid,id)
        games[gameId][0] = time.time()    
        print(id)
        emit('cookie',{'id':id})
        join_room(gameId)
        emit('message',{'state':'waiting_for_one_player'})
        if(games[gameId][1].state == 1):
            emit('message',{'state':'playing_game','board':games[gameId][1].getBoardString(), 'move':False, 'color':games[gameId][1].toMove[0]}, room=gameId)
            emit('message',{'state':'playing_game','board':games[gameId][1].getBoardString(), 'move':True, 'color':games[gameId][1].toMove[0]}, room=games[gameId][1].toMove[1])
        return
    emit('message',{'state':'no_room_found'})

@socketio.on('move')
def handleMove(data): 
    try:
        print(data)
        gameId = data['gameId']
        game = games[gameId][1]
        move = int(data['move'])
        game.placeTile(move)
        
    except:
        emit('message',{'state':'playing_game','board':games[gameId][1].getBoardString(), 'move':True, 'error':'Row already full', 'color':games[gameId][1].toMove[0]}, room=request.sid)
        return

    if(game.checkForWin()):
        data = registerGame(game.getBoardString(), games[gameId][1].players, games[gameId][1].toMove[1])
        error= data['message']
        emit('message',{'state':'game_end','board':games[gameId][1].getBoardString(), 'move':False, 'winner':False , 'draw':False, 'error':error}, room=gameId)
        emit('message',{'state':'game_end','board':games[gameId][1].getBoardString(), 'move':False, 'winner':True , 'draw':False}, room=games[gameId][1].toMove[1])
        game.changeState()
        return

    if(game.checkForDraw()):
        emit('message',{'state':'game_end','board':games[gameId][1].getBoardString(), 'move':False, 'winner':False , 'draw':True}, room=gameId)
        game.changeState()
        return

    game.changeToMove()
    emit('message',{'state':'playing_game','board':games[gameId][1].getBoardString(), 'move':False, 'color':games[gameId][1].toMove[0]}, room=gameId)
    emit('message',{'state':'playing_game','board':games[gameId][1].getBoardString(), 'move':True, 'color':games[gameId][1].toMove[0]}, room=games[gameId][1].toMove[1])
    return
                        
    
    
@socketio.on('disconnect')
def handleLeave():
    @copy_current_request_context
    def AbandonGame(userRoom,id):
        samebrowser = True
        firstid = games[userRoom][1].players[0][2]
        for x in games[userRoom][1].players:
            print(x)
            if(x[2] != firstid):
                samebrowser = False
                print("lenkai")
        print(samebrowser)
        if(samebrowser == False):
            time.sleep(15)
        for x in games[userRoom][1].players:
            if(x[1] == id):
                emit('message',{'state':'game_end','board':games[userRoom][1].getBoardString(), 'move':False, 'winner':True , 'draw':False, 'error':'opponent disconnected'}, room=userRoom)
                games[userRoom][1].changeState()

    userRoom = rooms(request.sid)[0]
    if(len(userRoom) != 8):
        userRoom = rooms(request.sid)[1]
   
    if userRoom not in games:
        return
  
    for x in games[userRoom][1].players:
        if(x[1] == request.sid):
           thread = Thread(target = AbandonGame , args = (userRoom,request.sid))
           thread.start()

    leave_room(userRoom)

