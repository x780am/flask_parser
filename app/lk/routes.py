from flask import render_template, redirect, flash, url_for, request, current_app
from flask_login import current_user, login_required
from app.lk import bp

from app.main.forms import EmptyForm
from app.auth.models import User


@bp.route('/', methods=['GET'])
def lk_home():
    return render_template("lk/index.html", title='API')


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
