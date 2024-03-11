from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import random
import time

app = Flask(__name__)
socketio = SocketIO(app)

# Dictionary to store active rooms
rooms = []

@app.route('/getRoom')
def getRoom():
    game_id ="".join(generate_game_id()) 
    rooms.append((game_id,time.time(),0))
    return {'game_id':game_id}

def generate_game_id():
    characters = "qwertyuiopasdfghjklzxcvbnm123456789"
    return random.sample(characters,8)

