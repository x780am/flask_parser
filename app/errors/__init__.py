from flask import Blueprint

bp = Blueprint('errors', __name__, template_folder='templates', static_folder='static', static_url_path='/errors/static')

# Этот импорт находится внизу, чтобы избежать циклических зависимостей.
from app.errors import routes