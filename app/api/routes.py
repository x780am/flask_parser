from flask import render_template, redirect, flash, url_for, request, current_app
from flask_login import current_user, login_required
from app.api import bp

@bp.route('/', methods=['GET'])
def api_home():
    return render_template("api/index.html", title='API')