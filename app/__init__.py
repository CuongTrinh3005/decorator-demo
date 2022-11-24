from flask import Blueprint
from flask_restx import Api

from .main.controller.auth_controller import api as auth_ns
from .main.controller.user_controller import api as user_ns


blueprint = Blueprint("api", __name__)

api = Api(
    blueprint,
    title="A short decorator demo",
    version="1.0",
    description="Python Decorators - Intermediate Python",
)

api.add_namespace(user_ns, path="/users")
api.add_namespace(auth_ns, path="/auth")
