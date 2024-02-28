from flask_login import login_user, logout_user, current_user
from flask import render_template, redirect, url_for, flash, request
from urllib.parse import urlsplit

from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, \
    ResetPasswordRequestForm, ResetPasswordForm
from app.auth.models import User
from app.auth.email import send_password_reset_email

@bp.route('/login', methods=['GET', 'POST'])
def login():  
        
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User().get(login=form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Неправильный логин или пароль')
            return redirect(url_for('auth.login'))
        user.update_when_login_user(ip=request.environ['REMOTE_ADDR'])
        # login_user(user, remember=form.remember_me.data)
        login_user(user, remember=True)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Войти', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():        
        if User().add(login=form.email.data, password=form.password.data, ip=request.environ['REMOTE_ADDR']):
            flash('Поздравляем, регистрация прошла успешно!!')
            return redirect(url_for('main.login'))
    return render_template('auth/register.html', title='Регистрация', form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User().get(login=form.email.data)
        if user:
            send_password_reset_email(user)
            # Вы можете заметить, что мигающее сообщение отображается, 
            # даже если адрес электронной почты, указанный пользователем, неизвестен. 
            # Это сделано для того, чтобы клиенты не могли использовать эту форму, 
            # чтобы выяснить, является ли данный пользователь участником или нет.
        flash('Отправили инструкцию с востановлением пароля на указанный email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title='Сброс пароля', form=form)
    
@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # я сначала проверяю, что пользователь не вошел в систему
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        if user.update_password(new_password=form.password.data):            
            flash('Ваш пароль сохранен')
            return redirect(url_for('auth.login'))
        else:
            flash('Ошибка при смене пароля')
    return render_template('auth/reset_password.html', form=form)
