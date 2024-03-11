import time
import random
from flask import Flask, Response, request
from WebSocket import webSocket
from WebSocket.webSocket import app


@app.route('/time')
def get_current_time():
    
    return {'time': time.time()}

@app.route('/send', methods=['POST'])
def get_data():
    print('Recieved from client: {}'.format(request.data))
    return Response('We recieved something…')


