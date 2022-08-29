from flask import current_app
from flask_mail import Message
from threading import Thread
from . import mail

def send_reset_password_mail(user, token):
    msg = Message('Confirm Email', 
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[user.email])

def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except:
            print("[MAIL SERVER] not working")


def send_email(subject, sender, recipients, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()