from flask import Blueprint

bp = Blueprint('help', __name__, template_folder='templates', static_folder='static')

from app.help import routes