import secrets 
import os 
from PIL import Image
from flask import url_for 
from flask_mail import Message
from Flask_app import mail 
from flask import current_app

def save_picture(form_picture):
    randm_hex = secrets.token_hex(10)
    _ , f_ext = os.path.splitext(form_picture.filename)
    picture_fname = randm_hex+f_ext 
    picture_path = os.path.join(current_app.root_path,'static/profile_pics',picture_fname)
    output = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output)
    i.save(picture_path)
    return picture_fname


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request",sender='noreply@demo.com',recipients=[user.email])
    msg.body = f"""
      To reset password visit the following link:{url_for('reset_token',token=token,_external=True)}
      if you did not make this request ignore the email
     """
    mail.send(msg)