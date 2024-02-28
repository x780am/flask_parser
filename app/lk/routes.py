from flask import render_template, redirect, flash, url_for, request, current_app, abort
from flask_login import current_user, login_required
from app.lk import bp

from app.main.forms import EmptyForm
from app.auth.models import User
from app.main.models import Query_db


@bp.route('/', methods=['GET'])
@login_required
def lk_home():
    return render_template("lk/index.html")

@bp.route('/messages', methods=['GET'])
@login_required
def messages():
    return render_template("lk/messages.html")


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User().get(login=username)    
    form = EmptyForm()
    return render_template('lk/user.html', user=user, form=form)


@bp.route('/update/<username>', methods=['POST'])
@login_required
def update(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User().get(login=username)
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('main.index'))
        if user != current_user:
            flash('You cannot update not yourself!')
            return redirect(url_for('lk.user', username=current_user.login))
        user.update_when_login_user(ip=request.environ['REMOTE_ADDR'])
        flash(f'You are update {username}!')
        return redirect(url_for('lk.user', username=username))
    else:
        return redirect(url_for('lk.index'))
    
@bp.route('/payments', methods=['GET'])
@login_required
def payments():
    user_id = current_user.id
    columns = Query_db().get_user_payments(user_id=user_id, get_columns=True)
    if columns == 404:
        return abort(404)
    
    return render_template('lk/payments.html', 
                           data_url = f'/admin/get_user_payments_data/{user_id}', 
                           limit_row = 15,
                           method = 'POST',
                           columns = columns,
                           header=f'История платежей'
                           )
    
@bp.route('/orders', methods=['GET'])
@login_required
def orders():
    user_id = current_user.id
    columns = Query_db().get_user_orders(user_id=user_id, get_columns=True)
    if columns == 404:
        return abort(404)
    
    return render_template('lk/orders.html', 
                           data_url = f'/admin/get_user_orders_data/{user_id}', 
                           limit_row = 15,
                           method = 'POST',
                           columns = columns,
                           header=f'История заказов'
                           )

