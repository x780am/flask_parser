from flask import render_template, redirect, flash, url_for, request, current_app
from flask_login import current_user, login_required

from app.main.forms import EmptyForm
from app.auth.models import User
from app.main import bp


# @app.before_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.last_seen = datetime.now(timezone.utc)
#         db.session.commit()

@bp.route('/test1')
def test1():
    current_app.logger.info('Вошли в test')
    current_app.logger.error('Вошли в test')
    return "test"
                

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    
    return render_template("index.html", title='Home Page')


    
from app.email import send_email
@bp.route('/send_mail', methods=['GET'])
def send_mail():
    
    current_app.logger.critical('Тест critical сообщения от модуля logger')
    
    send_email('Тестовое сообщение от модуля send_email',
               sender="support@parser24.online",
               recipients=["support@parser24.online"],
               text_body='text body', 
               html_body='<h1>HTML body</h1>')
    
    return 'Отправили 2 сообщения на почту админа, проверь'


@bp.route('/test', methods=['GET'])
def test():
    print(current_app.url_map)
    return 'current_app.url_map'