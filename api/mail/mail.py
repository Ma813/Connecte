"""This file contains the methods to send emails to users."""

from flask_mail import Message
from flask import Blueprint
from extensions import mail


emailer = Blueprint(name="email", import_name=__name__)


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

    mail.send(msg)


def sendNewPassword(email, password, username):
    """This method sends a new password to the user with a specific email and username"""
    msg = Message(
        "Your new Connectė account password", sender="Connectė", recipients=[email]
    )
    body = f"""
    Hello, {username}!
    
    Your Connectė account password has been reset. Your new password is:
    
    {password}
    
    We recommend changing it, however, the feature to change your password is expected to come in a later update to the game. Expected date for update is May 16th.
    """
    msg.body = body

    mail.send(msg)
