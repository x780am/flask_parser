from flask import Blueprint

bp = Blueprint('comments', __name__, template_folder='templates', static_folder='static')

from app.comments import routes