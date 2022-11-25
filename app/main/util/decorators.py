import logging
import time
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


def time_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print("%r - %.6f ms" % (func.__qualname__, (end_time - start_time) * 1000))
        return result

    return wrapper


def log_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.basicConfig(
            filename="logs/app.log",
            level=logging.INFO,
            format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
        )
        logging.getLogger().setLevel(logging.INFO)
        try:
            user_data, _ = Auth.get_logged_in_user(request)
            user = user_data.get("data")
            username = user.get("username")
            logging.info(f"User '{username}' used {func.__qualname__}")
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logging.exception(
                f"Exception raised in {func.__name__} exception: {str(e)}"
            )
            raise e

    return wrapper


def log_it_with_file_specified(logfile="logs/app.log"):
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            logging.basicConfig(
                filename=logfile,
                level=logging.INFO,
                format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
            )
            logging.getLogger().setLevel(logging.INFO)
            try:
                user_data, _ = Auth.get_logged_in_user(request)
                user = user_data.get("data")
                username = user.get("username")
                logging.info(f"User '{username}' used {func.__qualname__}")
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                logging.exception(
                    f"Exception raised in {func.__name__} exception: {str(e)}"
                )
                raise e

        return wrapped_function

    return logging_decorator


def cache_it(func):
    memo = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return memo[args]
        except KeyError:
            result = func(*args, **kwargs)
            memo[args] = result
            return result

    return wrapper
