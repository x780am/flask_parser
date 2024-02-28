from flask import render_template, redirect, jsonify, flash, url_for, request, current_app, send_file, Response, session
from flask_login import current_user, login_required
from app.main.forms import SubscribeForm, ContactForm
from app.main import bp

# запускается перед каждым запросом к экземпляру приложения.
# @bp.before_request
# def before_request():
    # current_app.logger.debug('Request Headers: %s', request.headers)
    # current_app.logger.debug('Request Data: %s', request.get_data())
    # current_app.logger.debug(f'[{request.method}] : {request.url}')
    # current_app.logger.debug('Request : %s', str(request.cookies))
    # current_app.logger.debug('Request : %s', Response.status)
    # current_app.logger.debug('session : %s', session)
    

# запускается после каждого запроса к экземпляру приложения.
# @bp.after_request()
# def after_request():
#     pass

# # регистрирует функцию, которая будет запускаться в конце каждого запроса.
# @bp.teardown_request()
# def teardown_request():
#     pass


@bp.route('/politics')
def politics():
    return render_template("politics.html")

@bp.route('/rules')
def rules():
    return render_template("rules.html")

@bp.route('/comments')
def comments():
    return render_template("comments.html")

@bp.route('/help')
def help():
    return render_template("help.html")

@bp.route('/parser')
def parser():
    return render_template("parser.html")

@bp.route('/test_logger')
def test():
    #  тест logger
    current_app.logger.debug('Test debug message')
    current_app.logger.info('Test info message')
    current_app.logger.warning('Test warning message')
    current_app.logger.error('Test error message')
    current_app.logger.critical('Test critical message')
    print('Test print message')
    return "test_logger"
                

@bp.route('/')
# @bp.route('/index')
def index():    
    return render_template("index.html", contact_form=ContactForm())

    
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


@bp.route('/subscribe', methods=['POST'])
def subscribe():
    subscribe_form=SubscribeForm()
    if subscribe_form.validate():
        return "Спасибо за подписку"
    else:
        return jsonify(subscribe_form.errors), 400
    

@bp.route('/contact', methods=['POST'])
def contact():
    contact_form=ContactForm()
    if contact_form.validate():
        print(contact_form.name.data, contact_form.email.data, contact_form.message.data)
        return "Сообщение отправлено"
    else:
        return jsonify(contact_form.errors), 400
    
    
@bp.route('/ip', methods=['GET'])  
def get_ip():
    ip = f"REMOTE_ADDR = {request.environ['REMOTE_ADDR']}"
    ip = ip + f"<br>remote_addr = {request.remote_addr}"
    ip = ip + f"<br>HTTP_X_REAL_IP = {request.environ.get('HTTP_X_REAL_IP', request.remote_addr)}"
    ip = ip + f"<br>X-Forwarded-For = {request.environ.get('X-Forwarded-For', request.remote_addr)}"
    ip = ip + f"<br>remote_addr = {request.remote_addr}"
    
    return ip
    # if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
    #     print(request.environ['REMOTE_ADDR'])
    # else:
    #     print(request.environ['HTTP_X_FORWARDED_FOR'])