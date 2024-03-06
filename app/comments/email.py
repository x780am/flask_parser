from flask import render_template, current_app
from app.email import send_email

    
def send_comment_answer_to_client(email, answer_text, comment_text):
    send_email(subject='Ответ на Ваш вопрос на Parser24.online',
               recipient=email,
               html_body=render_template('comments/email/comment_answer_to_client.html',
                                         answer_text=answer_text,
                                         comment_text=comment_text))

def send_comment_new_to_admin(name, email, message):
    send_email(subject='Новый комментарий на Parser24.online',
               html_body=render_template('comments/email/comment_new_to_admin.html',
                                         name=name,
                                         email=email,
                                         message=message))