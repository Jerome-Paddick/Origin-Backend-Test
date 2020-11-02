from flask_restful import Resource
from flask import request
from flask import current_app
from ..models.user import Users
from functools import wraps
import jwt

class AuthenticatedRestfulResource(Resource):
    """ resources extended with this class need a valid jwt to be accessed """

    def authenticate_token(self, func):
        """The token authentication"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                jwt_string = request.args.get('api_key')

                if not jwt_string:
                    return {"status": "not_authorized", "message": "No jwt provided"}, 401
                try:
                    JWT_SECRET_KEY = current_app.config.get('JWT_SECRET_KEY')
                    decoded_jwt = jwt.decode(jwt_string, JWT_SECRET_KEY, verify=True, algorithms=['HS256'])
                except jwt.ExpiredSignatureError:
                    return {"status": "jwt_expired", "message": "JWT expired"}, 401
                except jwt.exceptions.InvalidSignatureError:
                    return {"status": "not_authorized", "message": "Signature verification failed"}, 401

                self.user_id = decoded_jwt.get('user_id')
                self.user_email = decoded_jwt.get('email')
                self.jwt_exp = decoded_jwt.get('exp')

                return func(*args, **kwargs)
            except jwt.exceptions.DecodeError as ex:
                return {"status": "not_authorized", "message": "Invalid JWT token"}, 401
            except Exception as e:
                return {
                    "status": "auth_error",
                    "message": f"Unexpected auth error",
                    "error": str(e)
                }, 500

        return wrapper

    def __init__(self, **kwargs):
        self.method_decorators = [self.authenticate_token]
        self.user = None