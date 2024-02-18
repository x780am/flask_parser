from functools import wraps
from flask import abort
from flask_login import current_user

# проверка на админа. Если не админ, то 404, чтобы не было ощущения что страница есть
def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.is_admin:
            return func(*args, **kwargs)
        abort(404)

    return decorated_function