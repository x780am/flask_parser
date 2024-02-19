import bcrypt
import jwt
from hashlib import md5
from datetime import datetime
from time import time
from typing import Dict, Optional
from flask_login import UserMixin
from app.sql import MySql as mysql

from flask import current_app
from app import login



class User(UserMixin):
   
    def __init__(self):
        self.id = None
        self.password_hash = None
        self.login = None
        self.username = self.login
        self.password = None
        self.date_last = None
        self.is_admin = False
        self.balance = False
        
    # получить значение по user_id или login
    def get(self, user_id=None, login=None) -> Optional["User"]:
        # print(f'get.user_id={user_id}')
        if user_id or login:
            with mysql() as db:
                if user_id:
                    select_result = db.select_one('SELECT id, login, pass, date_last, balance FROM users where id= %(id)s ', {'id':user_id})
                elif login:
                    select_result = db.select_one('SELECT id, login, pass, date_last, balance FROM users where login= %(login)s', {'login':login})
                if select_result:                
                    self.password_hash = select_result['pass']
                    self.id = select_result['id']
                    self.login = select_result['login']
                    self.username = self.login 
                    self.date_last = select_result['date_last']
                    self.is_admin = True if self.id == 1 else  False
                    self.balance = select_result['balance']
                    return(self)
                else:                
                    self.id = None
                    self.password_hash = None
                    self.login = None
                    self.username = self.login 
                    self.password = None   
                    self.date_last =  None    
                    self.is_admin = False   
                    self.balance = False  
                    # print(db.error)
                    return(None)
        else:
            print("Не заполнены поля")
            return(None)
            
    # добавить пользователя в БД
    def add(self, login, password, ip='')-> Optional[bool]:
        # def set_password( password):
        #     return bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
        
        if login and password:
            with mysql() as db:
                password_hash = self.set_password(password)
                print(f"password_hash={password_hash}")
                select_result = db.insert('users', {'login': login, 'pass': password_hash, 'ip_reg': ip, 'hash_pass': 1})
                if not db.error and select_result:
                    self.get(user_id=select_result)                    
                    return True
                else:
                    print(db.error)
                    return False
        else:
            print("Не заполнены поля")
            return False
        
    # обновить пользователя в БД
    def update_when_login_user(self, ip)-> Optional[bool]:       
        if self.id and ip:
            ip_last = ip
            date_last = datetime.now()
            # print(f"date_last={date_last}, ip_last={ip_last}")
            with mysql() as db:
                select_result = db.update('users', {'ip_last': ip_last, 'date_last': date_last}, 'id=%(id)s', {'id': self.id})
                if select_result == 1:
                    # print(select_result)
                    return True
                else:
                    if db.error: 
                        print(db.error)
                    return False
        else:
            print("Не заполнены поля")
            return False
        
    # обновить пароль при сбросе
    def update_password(self, new_password):
        if new_password:
            with mysql() as db:
                password_hash = self.set_password(new_password)
                select_result = db.update('users', {'pass': password_hash}, 'id=%(id)s', {'id': self.id})
                if select_result == 1:
                    # print(select_result)
                    return True
                else:
                    if db.error: 
                        print(db.error)
                    return False
        
        
    def avatar(self, size)-> Optional[str]:
        digest = md5(self.login.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
                 
    def __str__(self) -> str:
        return f"<Id: {self.id}, login: {self.login}>"

    def __repr__(self) -> str:
        return self.__str__()  

    #  возвращает hash пароля
    @staticmethod
    def set_password( password):
        return bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
    
    # проверка пароля
    def check_password(self, password)-> Optional[str]:
        # print(f'password={password}, {self.password_hash}' )
        return bcrypt.checkpw(bytes(password, 'utf-8'), bytes(self.password_hash, 'utf-8'))
    
    # сгенерировать токен jwt для сброса пароля
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    # проверка токета jwt
    # статический метод, что означает, что его можно вызывать непосредственно из класса
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return None 
        return User().get(user_id=id)
    
            
@login.user_loader
def load_user(user_id: str) -> Optional[User]:
    return User().get(user_id=user_id)
