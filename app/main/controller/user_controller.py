import time

from flask import request
from flask_restx import Resource

from ..service.user_service import get_a_user
from ..service.user_service import get_all_users
from ..service.user_service import save_new_user
from ..util.decorators import admin_token_required, synchronized
from ..util.decorators import cache_it
from ..util.decorators import log_it
from ..util.decorators import time_it
from ..util.decorators import token_required
from ..util.dto import UserDto


api = UserDto.api
_user = UserDto.user


@api.route("/")
class UserList(Resource):
    @api.doc("list_of_registered_users")
    @api.marshal_list_with(_user, envelope="data")
    @admin_token_required
    @time_it
    @log_it
    def get(self):
        """List all registered users"""
        return get_all_users()

    @api.response(201, "User successfully created.")
    @api.doc("create a new user")
    @api.expect(_user, validate=True)
    @admin_token_required
    @time_it
    @log_it
    def post(self):
        """Creates a new User"""
        data = request.json
        return save_new_user(data=data)


@api.route("/<public_id>")
@api.param("public_id", "The User identifier")
@api.response(404, "User not found.")
class User(Resource):
    @api.doc("get a user")
    @api.marshal_with(_user)
    @token_required
    @time_it
    @log_it
    @cache_it
    @synchronized
    def get(self, public_id):
        """get a user given its identifier"""
        user = get_a_user(public_id)
        # time.sleep(3)
        if not user:
            api.abort(404)
        else:
            return user
