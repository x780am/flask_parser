
from flask_login import UserMixin
from app.sql import MySql as mysql

from flask import current_app


class Admin(UserMixin):
    # получить значение по user_id или login
    def get_all_users(self, page=1, per_page=10 ) :
        # per_page: количество элементов на странице
        with mysql() as db:
            has_prev = True if page > 1 else False
                
            offset = page*per_page - per_page
            limit = per_page
            
            count_users_data = db.select_one(f'SELECT count(id) as count_users FROM users', {})
            # print(f"count_users= {count_users_data['count_users']}")
            if count_users_data['count_users']:                
                has_next = True if count_users_data['count_users'] >= page * per_page + limit else False                
            
            # select_result = db.select('SELECT id, login FROM users limit %(limit)s offset %(offset)s', { 'limit ': 3, 'offset ':1 })
            select_result = db.select(f'SELECT id, login FROM users limit {limit} offset {offset}', {  })
            if select_result:   
                # print(dict(users=select_result, has_next=True, has_prev=True))             
                return(dict(users=select_result, has_next=has_next, has_prev=has_prev))
            else:                   
                print(db.error)                
                return(dict(users=None, has_next=False, has_prev=False))
      
 
