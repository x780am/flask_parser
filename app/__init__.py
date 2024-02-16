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
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if not app.debug and not app.testing:
    # if 1==1:
        if app.config['MAIL_SERVER']:
            # отправка писем админам
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            
            mail_handler = SMTPHandler(mailhost=app.config['MAIL_SERVER'], 
                                    fromaddr='support@parser24.online', # от кого
                                    toaddrs=app.config['ADMINS'], # кому
                                    subject='Microblog Ошибки', # Заголовок 
                                    credentials=auth, 
                                    secure=())
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
            # smtp.quit()
            
        # логирование в файл
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                        backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app


from app import models