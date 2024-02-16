"""
Автор: https://github.com/PyMySQL/PyMySQL
Установка: python -m pip install PyMySQL
Подключение: from lib.sql import MySql
"""
# coding: utf-8
import pymysql
import time
from config import Config

class MySql:
    def __init__(self, config=None):
        self.sql_text = ''
        try_limit = 3  # кол-во попыток
        try_count = 1
        while True:
            try:               
                self._conn = pymysql.connect(host=Config.MYSQL_HOST,
                                             user=Config.MYSQL_USER,
                                             password=Config.MYSQL_PASSWORD,
                                             db=Config.MYSQL_DB,
                                             charset='utf8mb4',
                                             cursorclass=pymysql.cursors.DictCursor,
                                             connect_timeout=600,
                                             local_infile=1)  # 600 = 10 мин
                
                self._cursor = self._conn.cursor()
                self.error = ''
                if self._conn:
                    break  # если все хорошо - выходим из цикла
            except Exception as e:
                try_count += 1
                if try_count > try_limit:
                    self.error = f"Сделали {try_limit} попытки, но неудачно, выходим. mysql Connect Error: {e}"
                    # print(self.error)
                    break  # выходим из цикла
                else:
                    # print(f"[Попытка №{try_count}] mysql Connect Error: {e}")
                    time.sleep(5)

    def __enter__(self):
        return self

    # чтобы можно было сделать with MySql(config) as db:
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._commit()
        self.connection.close()
        # print('in exit')

    # вывод ошибки
    def error(self):
        return self.error

    @property
    def sql_txt(self):
        return self.sql_text

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def _commit(self):
        self.connection.commit()   

    def select(self, sql_query, params=None):
        """
        Запрос к БД с выводом всех строк в списке
        Результат список словарей [{},{}]

        select_result = db.select('SELECT * FROM cron where id=%(id)s', {'id':'1',})
        if not db.error:
            print(select_result)
        else:
            print(db.error)
        """
        self.error = ''
        if self.error:
            return []

        if not sql_query:
            self.error = 'Не заполнены обязательные параметры'
            return []

        count_while = 0
        try:
            while True:
                count_while = count_while + 1
                if count_while > 5:
                    self.error = f'select. 5 попытки устранить Deadlock не хватило, выходим. sql_query={sql_query}, params={params}'
                    print(f'select. 5 попытки устранить Deadlock не хватило, выходим. sql_query={sql_query}, params={params}')
                    return []
                try:
                    self.cursor.execute(sql_query, params or ())
                except pymysql.err.Error as err:
                    if err.args[1] == 'Deadlock found when trying to get lock; try restarting transaction'\
                            or err.args[1] == 'Lock wait timeout exceeded; try restarting transaction':
                        # print(f'поймали Deadlock {sql_query}')
                        time.sleep(1)
                        continue
                    else:
                        self.error = err.args[1]
                        return []
                else:
                    self.error=''
                    return self.cursor.fetchall()
        except Exception as e:
            print(f'Непредвиденная ошибка в select. sql_query={sql_query}, params={params}. {e}')

    def select_one(self, sql_query, params=None, insert=False, rowcount=False):
        """
        Запрос к БД с выводом первой строки в списке.
        Результат: список из 1 словаря [{}] или словарь {}
        rowcount = True - вывести количество обработанных строк

        select_result = db.select_one('SELECT * FROM cron where id=%(id)s', {'id':'1',})
        if db.error or not select_result:
            print(db.error)
        else:
            print(select_result)
        """
        if self.error:
            self.error = ''  # зачем учитывать ошибку предыдущего запроса?
            # return {}
        # print(sql_query)
        if not sql_query:
            self.error = 'Не заполнены обязательные параметры'
            return -1
        self.sql_text = sql_query
        self.error = ''
        count_while = 0
        try:
            while True:
                count_while = count_while + 1
                if count_while > 5:
                    self.error = f'select_one. 5 попытки устранить Deadlock не хватило, выходим. sql_query={sql_query}, params={params}'
                    print(f'select_one. 5 попытки устранить Deadlock не хватило, выходим. sql_query={sql_query}, params={params}')
                    return []
                try:
                    self.cursor.execute(sql_query, params or ())
                except pymysql.err.Error as err:
                    if err.args[1] == 'Deadlock found when trying to get lock; try restarting transaction' \
                            or err.args[1] == 'Lock wait timeout exceeded; try restarting transaction':
                        # print(f'поймали Deadlock {sql_query}')
                        time.sleep(1)
                        continue
                    else:
                        self.error = err.args[1]
                        return {}
                else:
                    if insert:
                        self.error=''
                        return self.cursor.lastrowid
                    if rowcount:
                        self.error=''
                        return self.cursor.rowcount
                    self.error=''
                    return self.cursor.fetchone()
        # try:
        #     self.cursor.execute(sql_query, params or ())
        # except pymysql.err.Error as err:
        #     self.error = err.args[1]
        #     return {}
        # else:
        #     if insert:
        #         return self.cursor.lastrowid
        #     return self.cursor.fetchone()

        except Exception as e:
            print(f'Непредвиденная ошибка в select. sql_query={sql_query}, params={params}. {e}')

    def update(self, table, sets, where='', params=None):
        """
        Обновление строки в таблице table
        Результат: число обработанных строк

        select_result = db.update('cron', {'comment': 'комментарий3', 'name': 'test3'}, 'id=%(id)s', {'id': '16'})
        if not db.error:
            print(select_result)
        else:
            print(db.error)
        """
        if self.error:
            return 0

        if not sets or not table:
            self.error = 'Не заполнены обязательные параметры'
            return -1
        self.error = ''
        set_str = ''
        #
        # if "NULL" in sql_query:
        #     sql_query = sql_query.replace('NULL', 'NULL')

        params_sql = params
        # нужно преобразовать в update `cron` set comment=%(comment)s, name=%(name)s where id=%(id)s
        # и param = {'id': '16', 'comment': 'комментарийr2', 'name': 'test1'}
        for key, value in sets.items():
            if value == 'NULL':
                # чтобы корректно передать  update `proxy` set type=NULL
                set_str = set_str + f', {key}={value}' if set_str else f'{key}={value}'
            else:
                set_str = set_str + f', {key}=%({key})s' if set_str else f'{key}=%({key})s'
                params_sql[key] = value  # добавление в словарь
        sql_query = f'update `{table}` set {set_str} where {where} '
        # print(sql_query, params_sql, '\n')
        '''
        try:
            self.cursor.execute(sql_query, params_sql or ())
            self._commit()
        except pymysql.err.Error as err:
            self.error = err.args[1]
            return 0
        else:
            return self.cursor.rowcount
        '''
        count_while = 0
        try:
            while True:
                count_while = count_while + 1
                if count_while > 5:
                    self.error = f'update. 5 попытки устранить Deadlock не хватило, выходим. sql_query={sql_query}, params={params}'
                    print(f'update. 5 попытки устранить Deadlock не хватило, выходим. sql_query={sql_query}, params={params}')
                    return []
                try:
                    self.cursor.execute(sql_query, params_sql or ())
                except pymysql.err.Error as err:
                    if err.args[1] == 'Deadlock found when trying to get lock; try restarting transaction' \
                            or err.args[1] == 'Lock wait timeout exceeded; try restarting transaction':
                        time.sleep(1)
                        continue
                    else:
                        self.error = err.args[1]
                        return 0
                else:
                    return self.cursor.rowcount
       
        except Exception as e:
            print(f'Непредвиденная ошибка в update. sql_query={sql_query}, params={params_sql}. {e}')

    def insert(self, table, values):
        """
        Добавление строки в таблицу table
        Результат: id добавленной строки

        select_result = db.insert('cron', {'comment': 'комментарий_new', 'name': 'test_new', 'stop': '1'})
        if not db.error:
            print(select_result)
        else:
            print(db.error)
        """

        if self.error:
            return 0

        if not values or not table:
            self.error = 'Не заполнены обязательные параметры'
            return -1
        self.error = ''
        field_str = ''
        values_str = ''
        params_sql = {}
        # нужно преобразовать в insert into `cron` (comment, name) values(%(comment)s, name=%(name)s)
        # и param = {'comment': 'комментарийr2', 'name': 'test1'}
        for key, value in values.items():
            field_str = field_str + f', {key}' if field_str else f'{key}'
            values_str = values_str + f', %({key})s' if values_str else f'%({key})s'
            params_sql[key] = value  # добавление в словарь
        sql_query = f'insert into `{table}` ({field_str}) values({values_str}) '
        # print(sql_query, params_sql, sep='\n')
        try:
            self.cursor.execute(sql_query, params_sql or ())
            self._commit()
        except pymysql.err.Error as err:
            self.error = err.args[1]
            return 0
        else:
            return self.cursor.lastrowid

    def delete(self, table, where_values):
        """
        Удаление строк из таблицы table
        Результат: число обработанных строк

        select_result = db.delete('cron', {'id': '22', 'stop': '1'})
        if db.error:
            print(db.error)
        else:
            print(select_result)
        """

        if self.error:
            return 0

        if not where_values or not table:
            self.error = 'Не заполнены обязательные параметры'
            return -1
        self.error = ''
        where_str = ''
        params_sql = {}
        # нужно преобразовать в delete from `cron` where id=%(id)s and name=%(name)s
        # и param = {'id': '16', 'name': 'test1'}
        for key, value in where_values.items():
            where_str = where_str + f' and {key}=%({key})s' if where_str else f'{key}=%({key})s'
            params_sql[key] = value  # добавление в словарь
        sql_query = f'delete from `{table}` where {where_str}'
        # print(sql_query, params_sql, sep='\n')
        try:
            self.cursor.execute(sql_query, params_sql or ())
            self._commit()
        except pymysql.err.Error as err:
            self.error = err.args[1]
            return 0
        else:
            return self.cursor.rowcount


# для проверки
def main():
    with MySql() as db:
        # select_result = db.select_one(f'SELECT * FROM cron1 where id={id} or id={2}')
        select_result = db.select_one('SELECT * FROM cron where id= %(id)s ', {'id':'1'})
        # select_result = db.update('cron', {'comment': 'комментарий3', 'name': 'test3'}, 'id=%(id)s', {'id': '16'})
        # select_result = db.delete('cron', {'id': '22', 'stop': '1'})
        # UPDATE `proxy` SET `type` = NULL WHERE `proxy`.`id` = 6087
        # select_result = db.update('proxy', {'type': 'NULL'}, 'id=%(id)s', {'id': '6087'})
        # print(db.connection.show_warnings())  # тут ошибки все
        if not db.error:
            print(select_result)
        else:
            print(db.error)


# выполнится только если будет запущен этот файл
if __name__ == '__main__':
    main()
