from flask import request
from flask_restx import Namespace, Resource

from project.container import user_service
from project.setup.api.models import user

api = Namespace('auth')


@api.route('/register/')
class RegisterView(Resource):
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def post(self):
        """
        Create new user.
        """
        data = request.json
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return 'Не указан email или пароль', 401
        else:
            return user_service.create_user(email=email, password=password), 201


@api.route('/login/')
class LoginView(Resource):
    def post(self):
        """
        Login user.
        """
        data = request.json
        if data.get("email") and data.get("password"):
            return user_service.check(email=data.get("email"),
                                      password=data.get("password")), 201
        else:
            return "Что-то пошло не так!", 401

    def put(self):
        """
        Update token.
        """
        data = request.json
        if data.get("access_token") and data.get("refresh_token"):
            return user_service.update_token(access_token=data.get("access_token"),
                                             refresh_token=data.get("refresh_token")), 201
        else:
            return "Что-то пошло не так!", 401
