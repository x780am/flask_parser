import os
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

from config import Config

mail = Mail()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = ('Страница доступна только авторизованным пользователям')

def create_app(config_class=Config):
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    login.init_app(app)
    mail.init_app(app)

    # Я поместил импорт проекта прямо над элементом, app.register_blueprint()
    # чтобы избежать циклических зависимостей.
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    # app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(auth_bp)
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    from app.lk import bp as lk_bp
    app.register_blueprint(lk_bp, url_prefix='/lk')

    # if not app.debug and not app.testing:
    if 1==1:
        if app.config['MAIL_SERVER']:
            # отправка писем админам
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            
            mail_handler = SMTPHandler(mailhost=app.config['MAIL_SERVER'], 
                                    fromaddr=app.config['ADMIN'], # от кого
                                    toaddrs=app.config['ADMIN'], # кому
                                    subject='Flask_parser Ошибки', # Заголовок 
                                    credentials=auth, 
                                    secure=())
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
            
        # логирование в файл
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/flask_parser.log', maxBytes=10240,
                                        backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Flask_parser startup')

    return app


from app.auth import models