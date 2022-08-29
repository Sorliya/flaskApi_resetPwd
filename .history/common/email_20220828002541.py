from flask_mail import Message
from app import mail
def send_reset_password_mail(user, token):
