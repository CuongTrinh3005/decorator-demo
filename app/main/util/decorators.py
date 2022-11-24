from flask import request
from functools import wraps

from app.main.service.auth_helper import Auth


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        user_data, status = Auth.get_logged_in_user(request)
        if not user_data.get("data") or user_data.get("status") != "success":
            return user_data, status

        return func(*args, **kwargs)

    return decorated


def admin_token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        user_data, status = Auth.get_logged_in_user(request)
        user = user_data.get("data")
        if not user or user_data.get("status") != "success":
            return user_data, status

        if not user.get("admin"):
            response = {"message": "Admin token is needed", "status": "fail"}
            return response, 403

        return func(*args, **kwargs)

    return decorated
