import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
        
    ###  Настройка БД  ###
    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_DB = os.environ.get('MYSQL_DB')
    
    # DEBUG = True
    
    ###  Настройка почтового сервера ###
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or  ''
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 465) 
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None or 1
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or ''
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or ''
    
    ADMINS = ['support@parser24.online']
       
    # количество элементов на странице
    USERS_PER_PAGE = 10
    
    