from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import pymysql

cors = CORS()

socketio = SocketIO()

da = SQLAlchemy()