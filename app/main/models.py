import jwt
import time 
from flask_login import current_user
from app.sql import MySql as mysql
from app.defs import get_now_unix
from flask import current_app, url_for
from app.main import json_data 
from hashlib import md5

class Query_db():
    # получить значение по user_id или login
    # def get_all_users(self, page=1, per_page=10 ) :
    #     # per_page: количество элементов на странице
    #     with mysql() as db:
    #         has_prev = True if page > 1 else False
                
    #         offset = page*per_page - per_page
    #         limit = per_page
            
    #         count_users_data = db.select_one(f'SELECT count(id) as count_users FROM users', {})
    #         # print(f"count_users= {count_users_data['count_users']}")
    #         if count_users_data['count_users']:                
    #             has_next = True if count_users_data['count_users'] >= page * per_page + limit else False                
            
    #         # select_result = db.select('SELECT id, login FROM users limit %(limit)s offset %(offset)s', { 'limit ': 3, 'offset ':1 })
    #         select_result = db.select(f'SELECT id, login FROM users limit {limit} offset {offset}', {  })
    #         if select_result:   
    #             # print(dict(users=select_result, has_next=True, has_prev=True))             
    #             return(dict(users=select_result, has_next=has_next, has_prev=has_prev))
    #         else:                   
    #             print(db.error)                
    #             return(dict(users=None, has_next=False, has_prev=False))
            
    # def get_users1(self, offset=0, limit=10, sort='', search='') :
    #     # per_page: количество элементов на странице
    #     with mysql() as db:       
    #         offset = 0 if offset < 0 else offset
    #         limit = 10 if limit < 0 else limit
    #         sql_where = f"where login like '%%{search}%%'" if search else ''
            
    #         count_users_data = db.select_one(f'SELECT count(id) as count_users FROM users', {})
    #         total = count_users_data['count_users']
            
    #         sql_sort = 'id' # по умолчанию
    #         # sort='-name' или sort='+name'
    #         if sort:
    #             sql_sort = sort[1:]
    #             sql_sort = sql_sort + ' desc' if '-' in sort else sql_sort + ' asc'
                
    #         # print(f'sql_sort = {sql_sort}')  
    #         # print(f'sql_where = {sql_where}')   
    #         sql = f"SELECT id, login, DATE_FORMAT(reg_date, '%%Y.%%m.%%d %%H:%%i:%%s') as reg_date FROM users {sql_where} order by {sql_sort} limit {limit} offset {offset} "
    #         print(f'sql = {sql}')
    #         select_result = db.select(sql, { })
    #         if select_result:              
    #             return(dict(data=select_result, total=total))
    #         else:                   
    #             print(db.error)                
    #             return(dict(data=None, total=0))
            
    def get_users(self, offset=0, limit=10, sort='', search='', get_columns=False) :                        
        if current_user.is_admin:
            columns = [
                {'id': 'id', 'name': 'id', 'sort':True, 'search':True},
                {'id': 'login', 'name': 'email', 'sort':False, 'search':True},
                {'id': 'balance', 'name': 'На счету', 'sort':True, 'search':False, 'formatter':'`${cell} ₽`'},
                {'id': 'pay_sum', 'name': 'Покупки', 'sort':True, 'search':False, 'formatter':'`${cell} ₽`'},
                {'id': 'ip_last', 'name': 'IP входа', 'sort':True, 'search':False},
                {'id': 'date_last', 'name': 'Дата входа', 'sort':False, 'sql_query': "DATE_FORMAT(date_last, '%%Y.%%m.%%d %%H:%%i:%%s') as date_last"},
                {'id': 'reg_date', 'name': 'Дата регистрации', 'sort':True, 'sort_default': 'desc', 'sql_query': "DATE_FORMAT(reg_date, '%%Y.%%m.%%d %%H:%%i:%%s') as reg_date"},
                {'id': 'discount_ads', 'name': 'Скидка', 'sort':True, 'search':False},
                {'id': 'status', 'name': 'Статус', 'sort':True, 'search':False},
                {'id': 'ref_user', 'name': 'Реферал', 'sort':True, 'search':True},
                {'id': 'ban', 'name': 'Бан', 'sort':True, 'search':False},
                #  <a class="btn btn-primary" onclick="alert( '${row.cells[0].data}');">Example</a>  
                {'id': 'buttons', 'name': 'Кнопки',
                'formatter': '''gridjs.html(`                    
                    <a class="btn btn-info" href="/admin/user_orders/${row.cells[0].data}" target="_blank"><i class="fa fa-list-alt" aria-hidden="true"></i> Заказы</a>
                    <a class="btn btn-info" href="/admin/user_payments/${row.cells[0].data}" target="_blank"><i class="far fa-money-bill-alt" aria-hidden="true"></i> Платежи</a>
                    `)
                ''',       
                },
                ]        
            if get_columns:                
                return columns
            else:
                return self._get_sqldata_for_table(offset=offset, limit=limit, sort=sort, search=search, columns=columns, table_name='users')
        else:
            return 404        
    
   
    def get_orders(self, offset=0, limit=10, sort='', search='', get_columns=False):              
        if current_user.is_admin:
            columns = [
                        {'id': 'id', 'name': 'Номер', 'sort':True, 'search':True, 'sort_default': 'desc'},
                        {'id': 'email', 'name': 'email', 'sort':True, 'search':True},
                        {'id': 'date', 'name': 'Дата', 'sort':True, 'search':False, 'sql_query': "DATE_FORMAT(date, '%%Y.%%m.%%d %%H:%%i:%%s') as date" },
                        {'id': 'url', 'name': 'Ссылка', 'sort':False, 'search':True},
                        ]
            if get_columns:                
                return columns
            else:
                return self._get_sqldata_for_table(offset=offset, limit=limit, sort=sort, search=search, columns=columns, table_name='order')    
        else:
            return 404
        
    
    def get_user_orders(self, user_id, offset=0, limit=10, sort='', search='', get_columns=False) :  
        if current_user.id == user_id or current_user.is_admin:
            columns = [
                        {'id': 'date', 'name': 'Дата', 'sort':True, 'search':False, 'sort_default': 'desc', 'sql_query': "DATE_FORMAT(date, '%%Y.%%m.%%d %%H:%%i:%%s') as date" },
                        {'id': 'id', 'name': 'Заказ', 'sort':True, 'search':True},
                        {'id': 'url', 'name': 'Ссылка', 'sort':True, 'search':True},
                        {'id': 'count', 'name': 'Кол-во', 'sort':True, 'search':True},
                        {'id': 'summa', 'name': 'Сумма', 'sort':True, 'search':True, 'formatter':'`${cell} ₽`'},
                        {'id': 'status', 'name': 'Статус', 'sort':True, 'search':True},
                        {'id': 'pay', 'name': 'Оплата', 'sort':True, 'search':True},
                    ]
            if get_columns:                
                return columns
            else:
                return self._get_sqldata_for_table(offset=offset, limit=limit, sort=sort, search=search, columns=columns, table_name='view_user_orders', user_id=user_id)
        else:
            return 404
           
    @staticmethod
    def _get_sqldata_for_table(offset=0, limit=10, sort='', search='', columns=[], table_name='', user_id=None):  
        """
        # id - это поле в БД, name - это название столбца, sort -сортировка - поля для таблицы
        # 'search':True - поиск по этим полям, 
        # 'sort_default': 'desc' ['desc' или 'asc'] - поле с сортировкой по умолчанию
        # 'hidden':True - скрытый столбец
        # 'sql_query': "DATE_FORMAT(date, '%%Y.%%m.%%d %%H:%%i:%%s') as date" - если надо вывести строку из базы 
        # с форматированием или условием, иначе берем из поля id
        # 'id': 'buttons' - значит поле с кнопками и надо задать 'formatter': '''gridjs.html(` 
        columns = [
                    {'id': 'id', 'name': 'Номер', 'sort':True, 'search':True, 'sort_default': 'desc', 'hidden':True},
                    {'id': 'email', 'name': 'email', 'sort':True, 'search':True},
                    {'id': 'date', 'name': 'Дата', 'sort':True, 'search':False, 'sql_query': "DATE_FORMAT(date, '%%Y.%%m.%%d %%H:%%i:%%s') as date" },
                    {'id': 'url', 'name': 'Ссылка', 'sort':False, 'search':True},
                    {'id': 'buttons', 'name': 'Кнопки',
                        'formatter': '''gridjs.html(`                    
                            <a class="btn btn-info" href="/admin/user_orders/${row.cells[0].data}" target="_blank"><i class="fa fa-list-alt" aria-hidden="true"></i> Заказы</a>
                            <a class="btn btn-primary" onclick="alert( '${row.cells[0].data}');">Example</a> 
                            `)
                        ''',  
                    ]
         return self._get_sqldata_for_table(offset=offset, limit=limit, sort=sort, search=search, columns=columns, table_name='view_user_orders', user_id=user_id)
        """
        if not table_name or not columns:
            print('[_get_sqldata_for_table] Ошибка. Не заполнены обязательные поля')
            return(dict(data=None, total=0))            
            
        # сортирка по умолчанию или id - оно всегда есть
        if not sort:
            sort = '-id'
            for column in columns:
                if 'sort_default' in column:
                    sort_default = column['sort_default']  # 'desc' или 'asc'
                    sort = '+' if sort_default=='asc' else '-'  + column['id']
                    break
            # print(f'sql_sort ={sql_sort}')    
                
       
        # задаем лимит и смещение
        # offset = 0 if offset < 0 else offset
        # limit = 10 if limit < 0 else limit
        if offset < 0:
            print(f'[_get_sqldata_for_table] Ошибка. offset = {offset}')
            return(dict(data=None, total=0))
        if limit < 0:
            print(f'[_get_sqldata_for_table] Ошибка. limit = {limit}')
            return(dict(data=None, total=0))
        params = {'limit': int(limit), 'offset': int(offset) }
            
        # поиск по полям
        sql_where = ''
        if search:
            search = search.strip() # удалить пробелы в начале и конце
            sql_where = "where ("
            for column in columns:
                if 'search' in column and column['search']:
                    if 'like' in sql_where:
                        sql_where = sql_where + f" or {column['id']} like %(search)s"
                    else:
                        sql_where = sql_where + f"{column['id']} like %(search)s"
            sql_where = sql_where + ')'
            params['search'] =f'%{search}%'            
        # print(f'sql_where={sql_where}')
        
        if user_id:
            if sql_where:
                sql_where = sql_where + f' and user_id=%(user_id)s'
            else:
                sql_where = f'where  user_id=%(user_id)s'
            
            params['user_id'] =f'{user_id}'
            
        sql_sort = ''  
        # сортировка. sort='-name' или sort='+name'
        if sort:            
            sort_field  = sort[1:]  # название столбца
            _sort_acs = sort[:1] # первый символ
            # проверка запроса, первый символ это + или -
            if _sort_acs not in ['-', '+']:
                print(f"[_get_sqldata_for_table] Ошибка в запросе. Сортировка не содержит в первом символе + или -. sort = {sort}")                
                return(dict(data=None, total=0))
            sort_acs = 'desc' if _sort_acs=='-' else 'asc'
            # так как я не могу вставить им столбца как параметр, 
            # а имя могут изменить в html, то проверю вручную по полям
            sort_exist = False
            for column in columns:
                if column['id'] == sort_field:
                    sort_exist = True
                    break
            if sort_exist:
                sql_sort = f' order by {sort_field} {sort_acs} '
            else:
                print(f"[_get_sqldata_for_table] Попытка sql инъекции в поле сортировки. sort = {sort}")                
                return(dict(data=None, total=0))
                
        #  определим поля для выгрузки
        sql_fields = ''
        for column in columns:
            if 'buttons' == column['id']:
                continue
            if 'sql_query' in column and column['sql_query']:
                sql_fields = sql_fields + column['sql_query'] +  ','
            else:
                sql_fields = sql_fields + column['id'] +  ','
        sql_fields = sql_fields[:-1] if sql_fields[-1:] == ',' else sql_fields  # удалили последнюю запятую
        # print(f'sql_fields={sql_fields}')    
                
        sql = f"SELECT {sql_fields} "\
                f"FROM `{table_name}` {sql_where} {sql_sort} "\
                f"limit %(limit)s offset %(offset)s "
        
        with mysql() as db:
             # определяем количество строк
            count_data = db.select_one(f'SELECT count(*) as count_rows FROM `{table_name}`', {})
            if count_data:              
                total = count_data['count_rows'] 
            else:                   
                print(f'[count_data] Ошибка: {db.error}')                
                total=0                     
              
            #  запрос к БД
            if current_app.debug: 
                print(f'sql = {sql}, params = {params}')
            select_result = db.select(sql, params)
            if select_result:              
                return(dict(data=select_result, total=total))
            else:                   
                print(db.error)                
                return(dict(data=None, total=0))
            
            
    def get_user_payments(self, user_id, offset=0, limit=10, sort='', search='', get_columns=False) : 
        # print(f'current_user.id ={current_user.id} {type(current_user.id)}')  
        # print(f'user_id ={user_id} {type(user_id)}')  
        if current_user.id == user_id or current_user.is_admin:
            columns = [
                        {'id': 'id', 'name': 'Заказ', 'sort':True, 'search':True, 'hidden':True,},
                        {'id': 'date_add', 'name': 'Дата', 'sort':True, 'search':False, 'sort_default': 'desc', 'sql_query': "DATE_FORMAT(date_add, '%%Y.%%m.%%d %%H:%%i:%%s') as date_add" },
                        {'id': 'sum', 'name': 'Сумма', 'sort':True, 'search':True, 'formatter':'`${cell} ₽`'},
                        {'id': 'comment', 'name': 'Описание', 'sort':True, 'search':True}
                        ]
            if get_columns:                
                return columns
            else:
                return self._get_sqldata_for_table(offset=offset, limit=limit, sort=sort, search=search, columns=columns, table_name='view_user_payments', user_id=user_id)
        else:
            return 404
            
    def get_payments(self, offset=0, limit=10, sort='', search='', get_columns=False):               
        if current_user.is_admin:
            columns = [
                        {'id': 'id', 'name': 'Заказ', 'sort':True, 'search':True, 'hidden':True,},
                        {'id': 'date_add', 'name': 'Дата', 'sort':True, 'search':False, 'sort_default': 'desc', 'sql_query': "DATE_FORMAT(date_add, '%%Y.%%m.%%d %%H:%%i:%%s') as date_add" },
                        {'id': 'user_id', 'name': 'user_id', 'sort':True, 'search':True},
                        {'id': 'email', 'name': 'email', 'sort':True, 'search':True},
                        {'id': 'sum', 'name': 'Сумма', 'sort':True, 'search':True, 'formatter':'`${cell} ₽`'},
                        {'id': 'comment', 'name': 'Описание', 'sort':True, 'search':True},
                        {'id': 'order_id', 'name': 'order_id', 'sort':True, 'search':True},
                        {'id': 'wallet_name', 'name': 'Кошелек', 'sort':True, 'search':True}, 
                        {'id': 'buttons', 'name': 'Кнопки',
                         'formatter': '''
                            gridjs.html(`                    
                                <a class="btn btn-info" href="/admin/user_orders/${row.cells[2].data}" target="_blank"><i class="fa fa-list-alt" aria-hidden="true"></i> Заказы</a>
                                <a class="btn btn-info" href="/admin/user_payments/${row.cells[2].data}" target="_blank"><i class="far fa-money-bill-alt" aria-hidden="true"></i> Платежи</a>
                            `)
                         ''',       
                },
                    ]
            if get_columns:                
                return columns
            else:
                return self._get_sqldata_for_table(offset=offset, limit=limit, sort=sort, search=search, columns=columns, table_name='view_payments')        
        else:
            return 404
        
    def get_doxod_day(self, offset=0, limit=10, sort='', search='', get_columns=False):           
        if current_user.is_admin:
            columns = [
                        {'id': 'date', 'name': 'Дата', 'sort':True, 'search':False, 'sort_default': 'desc', 'sql_query': "DATE_FORMAT(date, '%%Y.%%m.%%d') as date" },
                        {'id': 'sum', 'name': 'Потрачено', 'sort':True, 'search':True, 'formatter':'`${cell} ₽`'},
                        {'id': 'sum_pay', 'name': 'Оплачено', 'sort':True, 'search':True, 'formatter':'`${cell} ₽`'},
                        {'id': 'pay_sum_dop', 'name': 'Оплачено,доп.', 'sort':True, 'search':True, 'formatter':'`${cell} ₽`'},
                        {'id': 'orders', 'name': 'Заказы', 'sort':True, 'search':True},
                        {'id': 'clients', 'name': 'Клиенты', 'sort':True, 'search':True},
                        {'id': 'cnt_user', 'name': 'Новые клиенты', 'sort':True, 'search':True},
                        {'id': 'sder_sum_order', 'name': 'Сред.заказ', 'sort':True, 'search':True, 'formatter':'`${cell} ₽`'},
                        {'id': 'count_ads', 'name': 'Объявлений', 'sort':True, 'search':True},                          
                    ]
            if get_columns:                
                return columns
            else:
                return self._get_sqldata_for_table(offset=offset, limit=limit, sort=sort, search=search, columns=columns, table_name='view_doxod_day') 
        else:
            return 404
        
    def get_doxod_month(self, offset=0, limit=10, sort='', search='', get_columns=False):
        if current_user.is_admin:
            columns = [
                        {'id': 'date', 'name': 'Дата', 'sort':True, 'search':False, 'sort_default': 'desc'},
                        {'id': 'sum', 'name': 'Потрачено', 'sort':True, 'search':True, 'formatter':'`${cell} ₽`'},
                        {'id': 'sum_pay', 'name': 'Оплачено', 'sort':True, 'search':True, 'formatter':'`${cell} ₽`'},
                        {'id': 'pay_sum_dop', 'name': 'Оплачено,доп.', 'sort':True, 'search':True, 'formatter':'`${cell} ₽`'},
                        {'id': 'orders', 'name': 'Заказы', 'sort':True, 'search':True},
                        {'id': 'clients', 'name': 'Клиенты', 'sort':True, 'search':True},
                        {'id': 'orders_day', 'name': 'Заказов/день', 'sort':True, 'search':True},              
                        {'id': 'sum_day', 'name': 'Сумма/день', 'sort':True, 'search':True, 'formatter':'`${cell} ₽`'},  
                        {'id': 'clients_day', 'name': 'Клиентов/день', 'sort':True, 'search':True},                     
                        {'id': 'cnt_user', 'name': 'Новые клиенты', 'sort':True, 'search':True},                               
                        {'id': 'sder_sum_order', 'name': 'Сред.заказ', 'sort':True, 'search':True, 'formatter':'`${cell} ₽`'},      
                    ]
            if get_columns:                
                return columns
            else:
                return self._get_sqldata_for_table(offset=offset, limit=limit, sort=sort, search=search, columns=columns, table_name='view_doxod_month')        
        else:
            return 404
        
class Contact():
    def set_contact_data(name, email, message, ip):
        with mysql() as db:
            select_result = db.insert('contact', {'email': email, 'text': message, 'name': name, 'ip': ip})
            if not db.error:
                current_app.logger.info(f"Добавлен вопрос от клиента в БД с id={select_result}")
            else:
                current_app.logger.critical(f"Ошибка при добавлении вопроса от клиента в БД: {db.error}")                
        return True
    
class Subscribe():
    def set_subscribe_data(email, ip):
        with mysql() as db:
            select_result = db.insert('sign', {'email': email, 'ip': ip})
            if not db.error:
                current_app.logger.info(f"Добавлена новая подписка в БД с id={select_result}")              
            else:
                current_app.logger.critical(f"Ошибка при добавлении подписка в БД: {db.error}")
        return True
    

class Parser_data():
    """
    Класс с настройками и данными о парсере
    """
    def get_status_work(self):
        """
        Получить статус работы парсера и БД
        Вернется: dict(status='', status_text='')
        Пример:
        from app.main.models import Parser_data
        status_work = Parser_data().get_status_work()
        """
        with mysql() as db:
            select_db_work = db.select_one(f"SELECT status, msg FROM `db_work`", {})
            # print(select_db_work)
            if db.error:
                current_app.logger.critical(f"[Parser_data.get_status_work] Ошибка при запросе статуса БД: {db.error}")
                return dict(status='', status_text='')
            # 0 - не работает
            if select_db_work["status"] == 0:
                status = "danger"
                status_text = select_db_work["msg"] if select_db_work["msg"] else "Парсер временно не работает"
                return dict(status=status, status_text=status_text)
            
            select_cron = db.select_one(f"SELECT stop FROM `cron` where name='new'", {})
            if db.error:
                current_app.logger.critical(f"[Parser_data.get_status_work] Ошибка при запросе статуса работы: {db.error}")
                return dict(status='', status_text='')
            if 'stop' in select_cron and select_cron['stop'] == 1:
                status = "warning"
                status_text = "Новые заказы временно не принимаются!"
                return dict(status=status, status_text=status_text)
              
            select_result = db.select_one(f"select status_text, status from status_work where active=1", {})
            if db.error:
                current_app.logger.critical(f"[Parser_data.get_status_work] Ошибка при запросе статуса работы: {db.error}")
                return dict(status='', status_text='')
            if select_result and "status" in select_result and select_result["status"]:
                status = select_result["status"]
                status_text = select_result["status_text"]
                return dict(status=status, status_text=status_text)   
            else:
                return dict(status='', status_text='')        
        return dict(status='', status_text='')
    
    def get_price(self):
        price = float(current_app.config["PRICE"])
        price_kop = round(price*100)
        return dict(price_rub=price, price_kop=price_kop)
    
class MD5:
    """
    хеш номера заказа с солью
    MD5.get_hash(338139)
    MD5.check_hash(9097a880458c4a41f69211af0512e9d4,338139)
    """
    def __init__(self):
        self.salt = current_app.config["SALT"]
    def get_hash(self, data):
        data = self.salt + str(data)
        encrypt_data = md5(data.encode()).hexdigest()
        return encrypt_data
    def check_hash(self, hash, data):
        data = self.salt + str(data)
        if md5(data.encode()).hexdigest() == hash:
            return True
        else:
            return False
        
class Order():
    """
    Класс для работы с заказом
    """
    def __init__(self, id=None, hash=None):
        if hash:
            self.id = self.get_id_by_hash(hash)
            self.hash = hash
        if id:
            self.id = id
            self.hash = self.get_hash_by_id(id)
    
    def id(self):
        return self.id    
    
    def hash(self):
        return self.hash    
    
    @staticmethod
    def get_hash_by_id(order_id):
        salt = current_app.config["SALT"]
        data = salt + str(order_id)
        encrypt_data = md5(data.encode()).hexdigest()
        return encrypt_data
        
    # данные по заказу из БД
    def _get_data_in_db(self):
        with mysql() as db:
            # 'o.email, o.get_statistic, o.url as user_url, '\
            # 'l.run,  l.cancel_order,o.new2020,o.user_id, '\
            # 'l.rezume,l.pars_ads, l.old_phone as cnt_old_phone, l.all_ads, l.del_ads, '\
            sql = 'SELECT l.hash, l.get_ads, l.pay_ads, l.old_ads,'\
                        'l.no_phone_ads, l.anonym_ads, l.dubl_phone, l.error_ads, l.need_pars_seller, l.check_del,'\
                        'o.autoload_id, o.only_with_phone, o.date_pay, l.stop_negative_balance, o.count_real,'\
                        'l.order_id, l.url, l.status_id, s.name as status, l.xls_file,l.csv_file,l.csv_zip_file,'\
                        'o.vip, o.fields, o.limit_count, o.export_csv, o.free, ifnull(u.ban,0) as ban, '\
                        'o.phone_anonym, o.only_new, o.save_tag, o.param_in_col, o.phone_dubli, o.ads_dubli, o.seller_dubli, o.local_priority, o.only_new_phone,'\
                        'ifnull(o.parse_by_date,"") as parse_by_date, o.get_seller_data, date(o.date) as order_date, o.work as order_work,'\
                        'DATE_ADD(stop_negative_balance_date, INTERVAL 24 hour) as negative_hours_left,'\
                        '(case when ifnull(o.parse_by_date,"")="" then 0 else o.count_all_bez_limit end) as count_all_bez_limit'\
                    ' FROM `log` l inner join `status` s on s.id=l.status_id '\
                    ' inner join `order` o on o.id=l.order_id '\
                    ' left join `users` u on o.user_id=u.id '\
                    f' where l.hash=%(hash)s'
                
            select_order = db.select_one(sql, {'hash': self.hash})
            if db.error:
                current_app.logger.critical(f"[Order._get_data_in_db] Ошибка при запросе: {db.error}")
                return None
            return select_order
        
    # сообщение по заказу из БД
    def _get_order_message_in_db(self):
        with mysql() as db:
            sql = 'select comment, l.hash '\
                  'from order_comment t '\
                  f'inner join log l on l.order_id=t.order_id and l.status_id=4 and l.hash=%(hash)s '
                
            select_order_message = db.select_one(sql, {'hash': self.hash})
            if db.error:
                current_app.logger.critical(f"[Order._get_order_message_in_db] Ошибка при запросе: {db.error}")
                return None
            select_order_message_text = select_order_message["comment"]
            select_order_message_text += f'<br>Для повтора заказа нажмите <button type="button" id="repeat" '\
                f'onclick="order_repeat(\'{select_order_message["hash"]}\')">Повторить заказ</button>'
            
            return select_order_message_text
    
    def get_data(self):
        """
        Данные о заказе
        Order(id=338145).get_data()
        Вернет: словарь данных
        """
            
        if not self.hash:
            current_app.logger.critical(f"[Order.get_data] Не задан hash заказа")
            return None
        
        #********** получаем данные из БД **********
        select_order = self._get_data_in_db()
        
        print(f'select_order={select_order}')
        return_data = dict()
        
        #********** вывод заголовков с ошибками **********
        if not select_order:
            return dict(stop=1, stop_header=json_data.get_order_header_none())
            
        if select_order["ban"] == 1:
            return dict(stop=1, stop_header=json_data.get_order_header_ban())  
         
        return_data["stop"] = 0
        return_data["stop_header"] = ""         
        
        #********** названия полей текстом **********
        dopfields_name = ""
        return_data["fields_name"] = json_data.field_name_by_id(fields_id=select_order["fields"]) 
        dopfields_name_set = json_data.get_dopfields_name()
        for key, value in select_order.items():                
            if key in dopfields_name_set:
                if value == 1:
                    if dopfields_name:
                        dopfields_name = dopfields_name + '<br>' + dopfields_name_set[key]
                    else:
                        dopfields_name = dopfields_name_set[key]
        return_data["dopfields_name"] = dopfields_name        
        
        #********** поля из БД**********
        return_data["url"] = select_order["url"]
        return_data["status_id"] = select_order["status_id"]
        return_data["limit_count"] = select_order["limit_count"]
        return_data["order_date"] = select_order["order_date"]
        return_data["order_id"] = select_order["order_id"]
        return_data["status"] = select_order["status"]
        return_data["export_csv"] = select_order["export_csv"]
        return_data["parse_by_date"] = select_order["parse_by_date"]
        return_data["free"] = select_order["free"]
        return_data["url_short"] = return_data["url"][0:80] if len(return_data["url"]) > 80 else ""
        return_data["fields_name_short"] = return_data["fields_name"][0:80] if len(return_data["fields_name"]) > 80 else ""
            
        
        #********** добавим .'?1709718949 чтоб не кешировался файл ********** 
        for key, value in select_order.items():     
            if key in ["xls_file", "csv_file", "csv_zip_file"] and value:
                return_data[key] = f"{value}?{get_now_unix()}"
               
        # если выбрано парсить и без телефона, то не будем показывать что есть ошибки
        if select_order["only_with_phone"] == 0 and select_order["no_phone_ads"] > 0:
            return_data["no_phone_ads"] = 0
        else:
            return_data["no_phone_ads"] = select_order["no_phone_ads"]
        
        load_ads = 0  
        all_ads_pars = 0
        seller_dubli_count = 0 
           
        # если нужно парсить продавцов, то из общего числа спаршенный объявлений вычтем те что без продавцов
        # if select_order["get_seller_data"] == 1:
        #     return_data["get_ads"] = select_order["get_ads"] - select_order["need_pars_seller"]
        
        # если заказ завершен, то построим все от количества выгруженных
        if select_order["order_work"] == 3:
            # сколько выгружено - это известно точно
            load_ads = select_order["count_real"]
            if select_order["seller_dubli"] == 1:
                if select_order["limit_count"] > 0:
                    seller_dubli_count = select_order["pay_ads"] - (load_ads + select_order["old_ads"])
                else:
                    seller_dubli_count = select_order["get_ads"] - select_order["count_real"]  # 14 марта 2023 до этого было $seller_dubli_count=0;
            all_ads_pars = load_ads + select_order["old_ads"] + seller_dubli_count
        else:
            # а может $all_ads_pars = $all_ads_pars - но не всегда работает, особо плохо при резюме
            all_ads_pars = select_order["get_ads"] + select_order["no_phone_ads"] + select_order["old_ads"]
            load_ads  = select_order["get_ads"]
            if load_ads < 0:
                load_ads  = 0
            
            seller_dubli_count=0 

            # if select_order["seller_dubli"] and select_order["xls_file"] != '':
            #     new_0 = 0
            #     # $auth_data = $db->select("SELECT count(id) as cnt from z_ads_$order_id where new=0 ", array());
            #     # if (isset($auth_data[0]))
            #     #     $new_0 = $auth_data[0]['cnt'];
            #     # seller_dubli_count = $new_0 - load_ads;
            #     # $all_ads_pars = $all_ads_pars + seller_dubli_count;
            
            # else:
            #     seller_dubli_count=0                    
         
        # комментарий к заказу для пользователя
        comment_for_order = ''
        if select_order["parse_by_date"] and select_order["count_all_bez_limit"] > 0 and select_order["order_work"] < 3:                
           comment_for_order = f"По заказу будет обработано {select_order['count_all_bez_limit']}"\
                    f" объявлений, чтобы спарсить только объявления по дату {select_order['parse_by_date']}. Это займет какое-то время."\
                    f" Ожидаемое кол-во объявлений {select_order['pay_ads']}, точное значение будет известно только после парсинга."
            

        if select_order["stop_negative_balance"] == 1 and select_order["order_work"] < 3:
            queue_mess ='Заказ остановлен, так как на вашем балансе отрицательная сумма. '\
                    'Пополните баланс аккаунта и заказ запустится автоматически, в противном '\
                    f'случае заказ будет отменен {select_order["negative_hours_left"]}.'
        
        #********** поля для alert **********
        queue_mess = ""
        return_data["queue_mess"] = queue_mess
        admin_panel = ''
        if current_user.is_admin:
            admin_panel = "Панель Админа"
        return_data["admin_panel"] = admin_panel
        return_data["comment_for_order"] = comment_for_order
        return_data["message_for_order"] = self._get_order_message_in_db()
        
        # формируем строку 'Скачано объявлений:'        
        div_get_ads_dop = f"({select_order['count_all_bez_limit']}) " if select_order["count_all_bez_limit"] > 0 else ""
        div_get_ads = f"{all_ads_pars} из {select_order['pay_ads']} {div_get_ads_dop}объявлений(-я)"        
        
        # координаты для progressbar
        progressbar_ads_text = f"{all_ads_pars} из {select_order['pay_ads']}"
        progressbar_ads_coord = round(100 * all_ads_pars / select_order['pay_ads'])
        progressbar_ads_coord = 100 if progressbar_ads_coord > 100 else progressbar_ads_coord
        
        # формируем строку 'Подходят для выгрузки:'
        div_good_ads_dop = 'уникальных ' if select_order["ads_dubli"] == 1 else ""
        div_good_ads = f"{load_ads} {div_good_ads_dop}объявлений(-я)"
          
        # формируем строку 'Исключены из выгрузки:'
        div_no_ads = ''
        if select_order["only_new"] == 1:            
            div_no_ads += f'Объявления, скачанные ранее: {select_order["old_ads"]}'
        if select_order["seller_dubli"] == 1:
            div_no_ads += f'<br>' if div_no_ads else div_no_ads
            div_no_ads += f'Повторы продавцов: {seller_dubli_count}'
        
        #********** поля для div и progressbar **********
        return_data["div_get_ads"] = div_get_ads
        return_data["div_good_ads"] = div_good_ads
        return_data["div_no_ads"] = div_no_ads  
        return_data["progressbar_ads_text"] = progressbar_ads_text  
        return_data["progressbar_ads_coord"] = progressbar_ads_coord  
              
        # возвращаем словарь
        return return_data  
    
    # проверка токета в базе
    # статический метод, что означает, что его можно вызывать непосредственно из класса
    @staticmethod
    def get_id_by_hash(hash):
        with mysql() as db:
            sql = 'select order_id from log where hash=%(hash)s '
            select_order_id = db.select_one(sql, {'hash': hash})
            if db.error:
                current_app.logger.critical(f"[Order.get_id_by_hash] Ошибка при запросе: {db.error}")
                return None
            if not select_order_id or 'order_id' not in select_order_id or not select_order_id['order_id']:
                return None
            return select_order_id['order_id']
            