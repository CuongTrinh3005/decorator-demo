from flask import request
from flask_restx import Resource

from app.main.service.auth_helper import Auth

from ..util.decorators import token_required
from ..util.decorators import log_it_with_file_specified
from ..util.decorators import time_it
from ..util.dto import AuthDto


api = AuthDto.api
user_auth = AuthDto.user_auth


@api.route("/login")
class UserLogin(Resource):
    """
    User Login Resource
    """

    @api.doc("user login")
    @api.expect(user_auth, validate=True)
    @time_it
    def post(self):
        # get the post data
        post_data = request.json
        return Auth.login_user(data=post_data)


@api.route("/logout")
class LogoutAPI(Resource):
    """
    Logout Resource
    """

    @api.doc("logout a user")
    @time_it
    @token_required
    @log_it_with_file_specified(logfile="logs/out.log")
    def post(self):
        # get auth token
        auth_header = request.headers.get("Authorization")
        return Auth.logout_user(data=auth_header)
