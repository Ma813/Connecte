"""This file contains the methods to send emails to users."""

from threading import Thread
from flask_mail import Message
from flask import Blueprint, current_app
from extensions import mail


emailer = Blueprint(name="email", import_name=__name__)

def sendAsyncEmail(app, msg):
    """This method sends an email asynchronously"""
    with app.app_context():
        mail.send(msg)

def sendVerifyLink(email, verificationID, username):
    """This method sends a verification link to the user with a specific email and username.
    The verification link is used to verify the user's email."""

    msg = Message(
        "Verify your Connectė account email", sender="Connectė", recipients=[email]
    )
    body = f"""
    Hello, {username}!
    
    Click the following link to verify your email: http://localhost:3000/verify/{verificationID}
    If you do not verify your email, you will not be able to reset your password.
    
    
    If you did not create an account, please ignore this email.
    """
    msg.body = body

    app = current_app._get_current_object()
    thr = Thread(target=sendAsyncEmail, args=(app, msg))
    thr.start()


def sendNewPassword(email, password, username):
    """This method sends a new password to the user with a specific email and username"""
    msg = Message(
        "Your new Connectė account password", sender="Connectė", recipients=[email]
    )
    body = f"""
    Hello, {username}!
    
    Your Connectė account password has been reset. Your new password is:
    
    {password}
    
    We recommend changing it in the profile page.
    """
    msg.body = body
    
    app = current_app._get_current_object()
    thr = Thread(target=sendAsyncEmail, args=(app, msg))
    thr.start()

