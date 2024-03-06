import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    SECRET_KEY_ORDER = '56165165165jghkhg'
        
    ###  Настройка БД  ###
    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_DB = os.environ.get('MYSQL_DB')
    
    # DEBUG = True
    
    ###  Настройка почтового сервера ###
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or  ''
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 465) 
    MAIL_USE_TLS = int(os.environ.get('MAIL_USE_TLS')) or 0
    MAIL_USE_SSL = int(os.environ.get('MAIL_USE_SSL')) or 1
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or ''
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or ''
    
    ADMIN = os.environ.get('ADMIN_EMAIL')
    ADMINS = [os.environ.get('ADMIN_EMAIL')]
    
    SUPPORT_EMAIL = os.environ.get('SUPPORT_EMAIL')
    
    PRICE = os.environ.get('PRICE')
       
    # количество элементов на странице
    USERS_PER_PAGE = 10
    COMMENTS_PER_PAGE = 5
    
    # защита от атак    
    # Secure ограничивает файлы cookie только трафиком HTTPS.
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE') or True    
    # True - cookie будут отправлены по зашифрованному каналу
    REMEMBER_COOKIE_SECURE = os.environ.get('REMEMBER_COOKIE_SECURE') or True
    # HttpOnly защищает содержимое файлов cookie от чтения с помощью JavaScript.
    SESSION_COOKIE_HTTPONLY = os.environ.get('SESSION_COOKIE_HTTPONLY') or True
    REMEMBER_COOKIE_HTTPONLY = os.environ.get('REMEMBER_COOKIE_HTTPONLY') or True
    # SameSite ограничивает отправку файлов cookie с запросами от внешних сайтов. 
    # Может быть установлено значение 'Lax'(рекомендуется) или 'Strict'. 
    # Lax предотвращает отправку файлов cookie с запросами CSRF с внешних сайтов, такими как отправка формы. 
    # Strict предотвращает отправку файлов cookie со всеми внешними запросами, включая переход по обычным ссылкам.
    SESSION_COOKIE_SAMESITE = os.environ.get('SESSION_COOKIE_SAMESITE') or 'Lax'
    # время жизни куки в секундах. 1 день=86400, 7 дней=604800
    PERMANENT_SESSION_LIFETIME = int(os.environ.get('PERMANENT_SESSION_LIFETIME')) or 86400
    
    

    
    