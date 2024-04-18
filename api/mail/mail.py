
# from WebSocket.webSocket import app
from flask import Flask, Response, request, Blueprint
from extensions import mail
from sqlalchemy.sql import text
from flask_mail import Message
import datetime

emailer = Blueprint(name="email", import_name=__name__)

def sendVerifyLink(email, verificationID, username):
    print(email)
    msg = Message('Verify your Connectė account email', sender = 'game.connecte@gmail.com', recipients = [email])
    body = f'''
    Hello, {username}!
    
    Click the following link to verify your email: http://localhost:3000/verify/{verificationID}
    If you do not verify your email, you will not be able to reset your password.
    
    
    If you did not create an account, please ignore this email.
    '''
    msg.body = body
    
    mail.send(msg)

