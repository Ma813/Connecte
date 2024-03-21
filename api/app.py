import time
import random
from flask import Flask, Response, request
from extensions import cors, socketio
from WebSocket.webSocket import room

def create_app(config=""):
    app = Flask(__name__)
    #app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    return app

def register_extensions(app):
    cors.init_app(app, resource={
    r"/*":{
        "origins":"*"
    }
    })
    socketio.init_app(app, cors_allowed_origins="*")

def register_blueprints(app):
    app.register_blueprint(room)
   

app = create_app()