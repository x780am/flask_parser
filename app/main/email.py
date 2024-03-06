from flask import render_template, current_app
from app.email import send_email

    
def send_contact_data_to_admin(name, email, message):
    send_email(subject='Вопрос на Parser24.online',
               html_body=render_template('email/admin_contact.html',
                                         name=name,
                                         email=email,
                                         message=message,
                                         admin=True))

def send_subscribe_data_to_admin(email):
    send_email(subject='Новая подписка на Parser24.online',
               html_body=render_template('email/admin_subscribe.html',
                                         email=email,
                                         admin=True))