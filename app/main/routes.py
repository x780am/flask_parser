import time
from flask import g, render_template, redirect, jsonify, flash, url_for, request, current_app, send_file, Response, session
from flask_login import current_user, login_required
from app.main.forms import SubscribeForm, ContactForm, FreeForm
from app.main import bp
from app.main.email import send_contact_data_to_admin, send_subscribe_data_to_admin
from app.utils import admin_required
from app.help.json_data import get_faq 
from app.comments.models import Comments
from app.main.models import Contact, Subscribe, Parser_data, Order

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
def index():
    free_form = FreeForm()
    # подстановка email зарегистрированному клиенту
    if not current_user.is_anonymous:
        free_form.email.data = current_user.login
    # для теста
    free_form.url.data = "avito.ru"
    free_form.email.data = "x780am@gmail.com"
        
    comments = Comments().get_comments(page=1, per_page=3, public_view=True)['comments']
    faqs = get_faq(support_email=g.support_email, only_index=True)
    status_work = Parser_data().get_status_work()
    price = Parser_data().get_price()
    return render_template("index.html", 
                           contact_form=ContactForm(),
                           faqs=faqs,
                           comments=comments,
                           free_form=free_form,
                           status_work=status_work,
                           price=price)
    
@bp.route('/free_order', methods=['POST'])
def free_order():
    free_form = FreeForm() 
    # print(free_form.email.data, free_form.url.data, free_form.checkPD.data)
    if free_form.validate():
        time.sleep(5)
        return 'Ваш заказ будет выполнен в ближайшее время.'\
                '<br>Увидеть ход выполнения заказа Вы можете на странице заказа №500715'\
                '<br>Отправили вам email с данными о заказе. Проверьте папку "Cпам", возможно оно там.'
    else:
        return jsonify(free_form.errors), 400
    """
        return {
        "email": [
            "Ошибка!"
        ]
        }
    """

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
        send_subscribe_data_to_admin(email=subscribe_form.email.data)
        Subscribe.set_subscribe_data(email=subscribe_form.email.data, 
                                   ip=g.ip_address)
        return "Спасибо за подписку"
    else:
        return jsonify(subscribe_form.errors), 400
    
@bp.route('/contact', methods=['POST'])
def contact():
    contact_form=ContactForm()
    if contact_form.validate():
        send_contact_data_to_admin(name=contact_form.name.data, 
                                   email=contact_form.email.data, 
                                   message=contact_form.message.data)
        Contact.set_contact_data(name=contact_form.name.data, 
                                   email=contact_form.email.data, 
                                   message=contact_form.message.data,
                                   ip=g.ip_address)
        return "Сообщение отправлено"
    else:
        return jsonify(contact_form.errors), 400

@bp.route('/ip', methods=['GET'])
def ip():
    return g.ip_address

@bp.route('/order/<token>', methods=['GET'])
def order(token):
    # order = Order(token=token).id
    # return str(order)
    # order = Order(token=token).get_data()
    # order = Order(id=338130).get_data() # free
    order = Order(id=338142).get_data() 
    print(order)
    return render_template("order.html", order=order)
    # token = Order(id=338145).get_order_token()
    # return token
    # order_data = Order(id=338145).get_data()
    # return order_data