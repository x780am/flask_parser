import math 
from flask_login import current_user
from app.sql import MySql as mysql
from flask import current_app, url_for
   
class Comments():
    def get_comments(self, page=1, per_page=10, public_view=False):
        # per_page: количество элементов на странице
        has_next = False
        has_prev = True if page > 1 else False
        offset = page*per_page - per_page
        limit = per_page
        
        if offset < 0:
            offset = 0
            # current_app.logger.error(f'[get_comments] Ошибка. offset = {offset}')
            # return(dict(comments=None, has_next=False, has_prev=False))
        if limit < 0:
            current_app.logger.error(f'[get_comments] Ошибка. limit = {limit}')
            return(dict(comments=None, has_next=False, has_prev=False))
        params = {'limit': int(limit), 'offset': int(offset) }
       
        with mysql() as db:            
            count_comments_data = db.select_one(f'SELECT count(id) as count_comments FROM comments where admin=0', {})
            if count_comments_data['count_comments']:  
                count_comments = int(count_comments_data['count_comments'])                
                max_page = math.ceil(count_comments/per_page)                    
                has_next = True if max_page > page else False 
                # current_app.logger.debug(f"max_page={max_page}, count_comments={count_comments}")
            
            # только опубликованные объявления и только для просмотра
            public_where = ''
            public_select = ''
            if public_view:
                public_where = ' and k1.public=1'
                public_select= ', 1 as public_view'            
                
            sql = f'SELECT k1.id, k1.name as user_name, k1.text, '\
                  f'concat(RPAD(LEFT(SUBSTRING_INDEX(k1.email, "@", 1), LENGTH(SUBSTRING_INDEX(k1.email, "@", 1))/2), LENGTH(SUBSTRING_INDEX(k1.email, "@", 1)), "*"),"@",SUBSTRING_INDEX(k1.email, "@", -1)) as user_email_public,'\
                  f'k1.email as user_email,'\
                  f'k1.date_add as user_date, k1.public, '\
                  f'k2.id as answer_id, k2.text as answer_text, k2.date_add as answer_date {public_select} '\
                  f'FROM comments k1 '\
                  f'left join comments k2 on k2.answer=k1.id '\
                  f'where k1.admin=0 {public_where} '\
                  f'order by k1.date_add desc '\
                  f"limit %(limit)s offset %(offset)s "
                  
            # current_app.logger.debug(f"sql={sql}. params={params}")     
            select_result = db.select(sql, params)
            if select_result:   
                # print(dict(comments=select_result, has_next=True, has_prev=True))             
                return(dict(comments=select_result, has_next=has_next, has_prev=has_prev))
            else:                
                if db.error:
                    current_app.logger.critical(f"Ошибка при получении списка комментариев: {db.error}")              
                return(dict(comments=None, has_next=False, has_prev=False))
            
    def comment_add(self, text, ip, email='', name='', admin=0, answer=0):   
        with mysql() as db:
            public = 1 if admin else 0
            name = 'Администратор' if admin else name
            email = '' if admin else email
            answer = answer if admin else 0        
            select_result = db.insert('comments', {'email': email, 
                                                   'text': text, 
                                                   'name': name, 
                                                   'ip': ip, 
                                                   'admin': admin,
                                                   'public': public,
                                                   'id_article': 1,
                                                   'answer': answer,
                                                   })
            if not db.error:
                current_app.logger.info(f"Добавлен отзыв в БД с id={select_result}")
            else:
                current_app.logger.critical(f"Ошибка при добавлении отзыва в БД: {db.error}")                
        return True 
    
    def comment_public(self, id, public):   
        with mysql() as db:
            public = 1 if public==1 else 0
            db.update('comments', {'public': public}, 'id=%(id)s', {'id': id})
            if not db.error:
                current_app.logger.info(f"Опубликован отзыв с id={id}")
                return True 
            else:
                current_app.logger.critical(f"Ошибка при публикации отзыва с id={id}: {db.error}")   
                return False 

    def comment_delete(self, id, admin=0):   
        with mysql() as db:
            db.delete('comments', {'id': id})
            if not db.error:
                # для админа удаляем только его отзыв, для клиента еще и ответ админа
                if not admin:
                    db.delete('comments', {'answer': id})
                    if not db.error:
                        current_app.logger.info(f"Удален отзыв с id={id}")
                        return True   
                else:
                    current_app.logger.info(f"Удален отзыв с id={id}")
                    return True                
            
        current_app.logger.critical(f"Ошибка при удалении отзыва с id={id}: {db.error}")   
        return False 

    def comment_edit(self, id, text):   
        with mysql() as db:
            # db.select('update text=%(text)s from comments where id=%(id)s', {'id':id, 'text':text})
            db.update('comments', {'text': text}, 'id=%(id)s', {'id': id})
            if not db.error:
                current_app.logger.info(f"Изменен отзыв с id={id}")
                return True 
            else:
                current_app.logger.critical(f"Ошибка при изменении отзыва с id={id}: {db.error}")   
                return False 
        
        
       
        
        
      
 
