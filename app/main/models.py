from flask_login import current_user
from app.sql import MySql as mysql

from flask import current_app, url_for


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
        
        
       
        
        
      
 
