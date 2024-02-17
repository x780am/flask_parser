from flask import render_template, redirect, flash, url_for, request, current_app
from flask_login import current_user, login_required

from app.main.forms import EmptyForm
from app.models import User, Admin
from app.main import bp


# @app.before_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.last_seen = datetime.now(timezone.utc)
#         db.session.commit()

@bp.route('/test1')
def test1():
    current_app.logger.info('Вошли в test')
    current_app.logger.error('Вошли в test')
    return "test"
                

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    
    return render_template("index.html", title='Home Page')


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User().get(login=username)    
    form = EmptyForm()
    return render_template('user.html', user=user, form=form)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    return 'Edit Profile'

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
            return redirect(url_for('main.user', username=current_user.login))
        user.update_when_login_user(ip=request.environ['REMOTE_ADDR'])
        flash(f'You are update {username}!')
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))
    
@bp.route('/all_users', methods=['GET'])
@login_required
def all_users():
    # users = [{'id': 1, 'login': 'user1'}, {'id': 2,'login': 'user2'},]
    page = request.args.get('page', 1, type=int)
    users = Admin().get_all_users(page=page, per_page=current_app.config['USERS_PER_PAGE'])
    if users and 'users' in users and users['users']:
        prev_url = url_for('main.all_users', page=page-1) if users['has_prev'] else None 
        next_url = url_for('main.all_users', page=page+1) if users['has_next'] else None
        return render_template('all_users.html', users=users['users'], next_url=next_url, prev_url=prev_url)
    else:
        return render_template('all_users.html', users=None, next_url=None, prev_url=None)

    
from app.email import send_email
@bp.route('/send_mail', methods=['GET'])
def send_mail():
    
    # current_app.logger.critical('Test critical message in logger')
    
    send_email('Test email send',
               sender="support@parser24.online",
               recipients=["support@parser24.online"],
               text_body='text body', 
               html_body='<h1>HTML body</h1>')
    
    return 'Send 2 message om admin email'
