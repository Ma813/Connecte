from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import pymysql

cors = CORS()

socketio = SocketIO()

da = SQLAlchemy()

mail = Mail()
