from flask import Blueprint

bp = Blueprint('lk', __name__, template_folder='templates', static_folder='static')


from app.lk import routes