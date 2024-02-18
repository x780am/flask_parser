from flask import render_template, redirect,  abort, flash, url_for, request, current_app
from flask_login import current_user, login_required
from app.admin import bp
from app.util import admin_required
from app.admin.models import Admin

@bp.route('/', methods=['GET'])
@admin_required
def admin_home():
    return render_template("admin/index.html", title='Admin home')
    
    
@bp.route('/all_users', methods=['GET'])
@admin_required
def all_users():
    page = request.args.get('page', 1, type=int)
    users = Admin().get_all_users(page=page, per_page=current_app.config['USERS_PER_PAGE'])
    if users and 'users' in users and users['users']:
        prev_url = url_for('admin.all_users', page=page-1) if users['has_prev'] else None 
        next_url = url_for('admin.all_users', page=page+1) if users['has_next'] else None
        return render_template('admin/all_users.html', users=users['users'], next_url=next_url, prev_url=prev_url)
    else:
        return render_template('admin/all_users.html', users=None, next_url=None, prev_url=None)
