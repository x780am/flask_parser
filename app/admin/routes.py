from flask import render_template, redirect,  abort, flash, url_for, request, current_app
from flask_login import current_user, login_required
from app.admin import bp
from app.util import admin_required
from app.main.models import Query_db

@bp.route('/', methods=['GET'])
@admin_required
def admin_home():
    return render_template("admin/index.html", title='Admin home')
    
    
# @bp.route('/all_users', methods=['GET'])
# @admin_required
# def all_users():
#     page = request.args.get('page', 1, type=int)
#     users = Query_db().get_all_users(page=page, per_page=current_app.config['USERS_PER_PAGE'])
#     if users and 'users' in users and users['users']:
#         prev_url = url_for('admin.all_users', page=page-1) if users['has_prev'] else None 
#         next_url = url_for('admin.all_users', page=page+1) if users['has_next'] else None
#         return render_template('admin/all_users.html', users=users['users'], next_url=next_url, prev_url=prev_url)
#     else:
#         return render_template('admin/all_users.html', users=None, next_url=None, prev_url=None)
    
    
@bp.route('/users', methods=['GET'])
@admin_required
def users():
    columns = Query_db().get_users(get_columns=True)
    
    return render_template('admin/users.html', 
                           data_url = '/admin/users_data', 
                           limit_row = 20,
                           method = 'POST',
                           columns = columns,
                           header='Список пользователей'
                           )

@bp.route('/users_data', methods=['GET', 'POST'])
@admin_required
def users_data():
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    sort = request.args.get('sort', type=str, default='')
    search = request.args.get('search', type=str, default='')
    
    users = Query_db().get_users(offset=start, limit=length, sort=sort, search=search)
    
    if users and 'data' in users and users['data']:
        return {'data': users['data'], 'total': users['total']}
    
    return {'data': None, 'total': 0}

        
@bp.route('/orders', methods=['GET'])
@admin_required
def orders():
    columns = Query_db().get_orders(get_columns=True)
    # print(columns)
    return render_template('admin/orders.html', 
                           data_url = '/admin/orders_data', 
                           limit_row = 15,
                           method = 'POST',
                           columns = columns,
                           header='Список заказов'
                           )
      

@bp.route('/orders_data', methods=['GET', 'POST'])
@admin_required
def orders_data():
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    sort = request.args.get('sort', type=str, default='')
    search = request.args.get('search', type=str, default='')
    
    orders = Query_db().get_orders(offset=start, limit=length, sort=sort, search=search)
    
    if orders and 'data' in orders and orders['data']:
        return {'data': orders['data'], 'total': orders['total']}
    
    return {'data': None, 'total': 0}

@bp.route('/user_orders/<user_id>', methods=['GET'])
@admin_required
def user_orders(user_id):
    user_id = int(user_id)
    columns = Query_db().get_user_orders(user_id=user_id, get_columns=True)
    if columns == 404:
        return abort(404)
    
    return render_template('admin/user_orders.html', 
                           data_url = f'/admin/get_user_orders_data/{user_id}', 
                           limit_row = 20,
                           method = 'POST',
                           columns = columns,
                           header=f'История заказов [{user_id}]'
                           )

@bp.route('/get_user_orders_data/<user_id>', methods=['GET', 'POST'])
@login_required
def get_user_orders_data(user_id):
    user_id = int(user_id)
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    sort = request.args.get('sort', type=str, default='')
    search = request.args.get('search', type=str, default='')
    
    users = Query_db().get_user_orders(user_id=user_id, offset=start, limit=length, sort=sort, search=search)
    if users == 404:
        return abort(404)
    if users and 'data' in users and users['data']:
        return {'data': users['data'], 'total': users['total']}
    
    return {'data': None, 'total': 0}


# @bp.route('/test', methods=['GET'])
# @admin_required
# def test():
#     return render_template('admin/test.html') 

# @bp.route('/users_data1', methods=['GET', 'POST'])
# @admin_required
# def users_data1():
#     start = request.args.get('start', type=int, default=-1)
#     length = request.args.get('length', type=int, default=-1)
#     sort = request.args.get('sort', type=str, default='')
#     search = request.args.get('search', type=str, default='')
    
#     users = Query_db().get_users1(offset=start, limit=length, sort=sort, search=search)
    
#     if users and 'data' in users and users['data']:
#         return {'data': users['data'], 'total': users['total']}
    
#     return {'data': None, 'total': 0}


@bp.route('/user_payments/<user_id>', methods=['GET'])
@admin_required
def user_payments(user_id):
    user_id = int(user_id)
    columns = Query_db().get_user_payments(user_id=user_id, get_columns=True)
    if columns == 404:
        return abort(404)
    
    return render_template('admin/user_payments.html', 
                           data_url = f'/admin/get_user_payments_data/{user_id}', 
                           limit_row = 20,
                           method = 'POST',
                           columns = columns,
                           header=f'История платежей [{user_id}]'
                           )

@bp.route('/get_user_payments_data/<user_id>', methods=['GET', 'POST'])
@login_required
def get_user_payments_data(user_id):
    user_id = int(user_id)
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    sort = request.args.get('sort', type=str, default='')
    search = request.args.get('search', type=str, default='')
    
    users = Query_db().get_user_payments(user_id=user_id, offset=start, limit=length, sort=sort, search=search)
    if users == 404:
        return abort(404)
    if users and 'data' in users and users['data']:
        return {'data': users['data'], 'total': users['total']}
    
    return {'data': None, 'total': 0}


@bp.route('/payments', methods=['GET'])
@admin_required
def payments():
    columns = Query_db().get_payments(get_columns=True)
    
    return render_template('admin/user_payments.html', 
                           data_url = '/admin/get_payments_data', 
                           limit_row = 20,
                           method = 'POST',
                           columns = columns,
                           header='Список платежей'
                           )

@bp.route('/get_payments_data', methods=['GET', 'POST'])
@admin_required
def get_payments_data():
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    sort = request.args.get('sort', type=str, default='')
    search = request.args.get('search', type=str, default='')
    
    return_data = Query_db().get_payments(offset=start, limit=length, sort=sort, search=search)
    
    if return_data and 'data' in return_data and return_data['data']:
        return {'data': return_data['data'], 'total': return_data['total']}
    
    return {'data': None, 'total': 0}


@bp.route('/doxod', methods=['GET'])
@admin_required
def doxod():
    columns = Query_db().get_doxod_day(get_columns=True)
    
    return render_template('admin/doxod.html', 
                           data_url = '/admin/get_doxod_data', 
                           limit_row = 10,
                           method = 'POST',
                           columns = columns,
                           header='Доход по дням'
                           )

@bp.route('/get_doxod_data', methods=['GET', 'POST'])
@admin_required
def get_doxod_data():
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    sort = request.args.get('sort', type=str, default='')
    search = request.args.get('search', type=str, default='')
    
    return_data = Query_db().get_doxod_day(offset=start, limit=length, sort=sort, search=search)
    
    if return_data and 'data' in return_data and return_data['data']:
        return {'data': return_data['data'], 'total': return_data['total']}
    
    return {'data': None, 'total': 0}


@bp.route('/doxod_month', methods=['GET'])
@admin_required
def doxod_month():
    columns = Query_db().get_doxod_month(get_columns=True)
    
    return render_template('admin/doxod_month.html', 
                           data_url = '/admin/get_doxod_month_data', 
                           limit_row = 10,
                           method = 'POST',
                           columns = columns,
                           header='Доход по месяцам'
                           )

@bp.route('/get_doxod_month_data', methods=['GET', 'POST'])
@admin_required
def get_doxod_month_data():
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    sort = request.args.get('sort', type=str, default='')
    search = request.args.get('search', type=str, default='')
    
    return_data = Query_db().get_doxod_month(offset=start, limit=length, sort=sort, search=search)
    
    if return_data and 'data' in return_data and return_data['data']:
        return {'data': return_data['data'], 'total': return_data['total']}
    
    return {'data': None, 'total': 0}
