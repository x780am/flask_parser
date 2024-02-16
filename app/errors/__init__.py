from flask import Blueprint

bp = Blueprint('errors', __name__)

# Этот импорт находится внизу, чтобы избежать циклических зависимостей.
from app.errors import handlers