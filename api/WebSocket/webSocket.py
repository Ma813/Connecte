from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
from flask_cors import CORS
import random
import time
from Connect4.connect4 import Connect4
app = Flask(__name__)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

socketio = SocketIO(app, cors_allowed_origins="*")

# Dictionary to store active rooms
games = {}

@app.route('/getRoom')
def getRoom():
    gameId ="".join(generateId(8)) 
    games[gameId] = [time.time(),Connect4()]
    return {'gameId':gameId}

def generateId(lenght):
    characters = "qwertyuiopasdfghjklzxcvbnm123456789"
    return random.sample(characters,lenght)

@socketio.on('join')
def handleJoin(data): 

    gameId = data['gameId']

 

    if gameId in games:
        if(games[gameId][1].state == 1):
            join_room(gameId)
            emit('message',{'state':'playing_game','board':games[gameId][1].getBoardString(), 'move':False}, room=gameId)
            return
        games[gameId][1].addPlayer(request.sid)
        games[gameId][0] = time.time()
        join_room(gameId)
        emit('message',{'state':'waiting_for_one_player'})
        if(games[gameId][1].state == 1):
            emit('message',{'state':'playing_game','board':games[gameId][1].getBoardString(), 'move':False}, room=gameId)
            emit('message',{'state':'playing_game','board':games[gameId][1].getBoardString(), 'move':True}, room=games[gameId][1].toMove[1])
        return
    emit('message',{'state':'no_room_found'})

@socketio.on('move')
def handleMove(data): 

    gameId = data['gameId']

    if gameId not in games:
        emit('message',{'state':'playing_game','board':games[gameId][1].getBoardString(), 'move':False, 'error':'Invalid game'}, room=request.sid)
        return

    game = games[gameId][1]

    if(game.state != 1):
        emit('message',{'state':'playing_game','board':games[gameId][1].getBoardString(), 'move':False, 'error':'Game is not in progress'}, room=request.sid)
        return

    if(request.sid != game.toMove[1]):
        emit('message',{'state':'playing_game','board':games[gameId][1].getBoardString(), 'move':False, 'error':'Wrong turn'}, room=request.sid)
        return

    if 'move' not in data:
        emit('message',{'state':'playing_game','board':games[gameId][1].getBoardString(), 'move':True, 'error':'no move sent'}, room=request.sid)
        return
    
    move = int(data['move'])
    
    if move not in game.legalMoves():
        emit('message',{'state':'playing_game','board':games[gameId][1].getBoardString(), 'move':True, 'error':'Invalid move'}, room=request.sid)
        return

    game.placeTile(move)
    
    if(game.checkForWin()):
        emit('message',{'state':'game_end','board':games[gameId][1].getBoardString(), 'move':False, 'winner':False , 'draw':False}, room=gameId)
        emit('message',{'state':'game_end','board':games[gameId][1].getBoardString(), 'move':False, 'winner':True , 'draw':False}, room=games[gameId][1].toMove[1])
        game.changeState()
        return

    if(game.checkForDraw()):
        emit('message',{'state':'game_end','board':games[gameId][1].getBoardString(), 'move':False, 'winner':False , 'draw':True}, room=gameId)
        game.changeState()
        return

    game.changeToMove()
    emit('message',{'state':'playing_game','board':games[gameId][1].getBoardString(), 'move':False}, room=gameId)
    emit('message',{'state':'playing_game','board':games[gameId][1].getBoardString(), 'move':True}, room=games[gameId][1].toMove[1])
    return
                        
    
    
@socketio.on('disconnect')
def handleLeave():

    userRoom = rooms(request.sid)[0]
    if(len(userRoom) != 8):
        userRoom = rooms(request.sid)[1]
   
    if userRoom not in games:
       
        return
  
    for x in games[userRoom][1].players:
        if(x[1] == request.sid):
            emit('message',{'state':'game_end','board':games[userRoom][1].getBoardString(), 'move':False, 'winner':True , 'draw':False, 'error':'opponent disconnected'}, room=userRoom)
            games[userRoom][1].changeState()

    leave_room(userRoom)