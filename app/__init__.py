import os
from flask import Flask, request, g
from flask_login import LoginManager
from flask_mail import Mail
import logging
from app import logger_set
from config import Config
from flask_paranoid import Paranoid
from flask_login import AnonymousUserMixin

mail = Mail()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = ('Страница доступна только авторизованным пользователям')
# мой параметр is_admin
class Anonymous(AnonymousUserMixin):
  def __init__(self):
    self.is_admin = False
login.anonymous_user = Anonymous

def create_app(config_class=Config):
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # создаем логгер с именем проекта и меняем его
    # logger = logging.getLogger(__name__)
    logger_set.set_logger(logger=logging.getLogger(__name__), config=app.config)
    
    # авторизация
    login.init_app(app)
    # отправка email
    mail.init_app(app)
    """При вышеуказанной настройке каждый раз, когда сеанс обнаруживается как исходящий с другого IP-адреса или 
    пользовательского агента, расширение блокирует запрос, очищает сеанс пользователя и файл cookie запоминания 
    Flask-Login (если он найден), а затем выполняет перенаправление. на корневой URL-адрес сайта."""
    if not app.debug:
        paranoid = Paranoid(app)
        paranoid.redirect_view = '/'

    # Я поместил импорт проекта прямо над элементом, app.register_blueprint()
    # чтобы избежать циклических зависимостей.
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    from app.lk import bp as lk_bp
    app.register_blueprint(lk_bp, url_prefix='/lk')
    
    from app.help import bp as help_bp
    app.register_blueprint(help_bp, url_prefix='/help')
    
    from app.comments import bp as comments_bp
    app.register_blueprint(comments_bp, url_prefix='/comments')
    
    # то что будет в каждом шаблоне при рендеринге
    from app.main.forms import SubscribeForm
    @app.context_processor
    def context_processor():
        return dict(subscribe_form=SubscribeForm())
    
    # ip пользователя
    @app.before_request
    def before_request():
        g.ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        g.support_email = app.config['SUPPORT_EMAIL']
        
    
    app.logger.info('Приложение Flask_parser запущено')
    return app


from app.auth import models