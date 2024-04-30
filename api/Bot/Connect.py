from Bot.Algorithim2 import AiPlayer
import websocket
from websocket import create_connection
import requests
import asyncio
import numpy as np
from threading import Thread
import socketio

def connectBotToGame(link,depth):
    algorithim = AiPlayer(depth)
    sio = socketio.SimpleClient()
    sio.connect('http://localhost:5000')
    thread = Thread(target = createConnection, args = (link,algorithim,sio))
    thread.start()


def createConnection(link,algorithim,sio):

    sio.emit('join', {'gameId': link,'id':"0",'token':"0"})
    
    while(True):
        event = sio.receive()
        if(event[0] == 'message'):
            if(event[1]['state'] == 'playing_game'):
                if(event[1]["move"]):
                    game = algorithim.setUpGame(int(event[1]["color"]),eval('np.array(' + event[1]["board"] + ')'))
                    sio.emit('move',{'gameId': link, 'move': algorithim.CalculateMove(game)})
                  
                    continue
            if(event[1]['state'] == 'game_end'):
                break