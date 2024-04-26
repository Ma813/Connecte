import time
import random
from flask import Flask, Response, request
from extensions import cors, socketio, da, mail
from WebSocket.webSocket import room
from DB.database import datab
from mail.mail import emailer
import config

def create_app(config=""):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    return app

def register_extensions(app):
    cors.init_app(app, resource={
    r"/*":{
        "origins":"*"
    }
    },
    CORS_SUPPORTS_CREDENTIALS = True
    )
    socketio.init_app(app, cors_allowed_origins="*")
    da.init_app(app)
    mail.init_app(app)

def register_blueprints(app):
    app.register_blueprint(room)
    app.register_blueprint(datab)
    app.register_blueprint(emailer)
   

app = create_app(config)