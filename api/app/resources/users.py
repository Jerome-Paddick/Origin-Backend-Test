from flask import current_app
from ..models.core import db
from ..models.user import Users
from flask_restful import reqparse, Resource
from flask_restful_swagger import swagger
from flask_restful import fields, inputs
from datetime import datetime, timezone, timedelta
import re
import jwt


@swagger.model
class LoginRequest:
    resource_fields = {
        "email": fields.String,
        "password": fields.String,
    }
    required = ["email", "password"]

class Login(Resource):
    @swagger.operation(
        # responseClass=LoginRequest.__name__,
        parameters=[
            {
                "dataType": LoginRequest.__name__,
                "name": "payload", "required": True, "allowMultiple": False, "paramType": "body",
            }
        ],
        responseMessages=[
            {"code": 200, "message": "Successful Request"},
            {"code": 400, "message": "Invalid Request"},
            {"code": 500, "message": "Unexpected error"},
        ]
    )
    def post(self):
        """ Generates jwt for user"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, required=True)
            parser.add_argument('password', type=str, required=True)
            args = parser.parse_args()
        except:
            return {'status': 'invalid_request', 'message': 'Email / password not provided'}, 400
        try:
            email = args.get('email')
            user = Users.query.filter(Users.email==email).first()

            if not user:
                return {'status': 'invalid_request', 'message': 'invalid email'}, 400

            if not user.check_password(args.get('password')):
                return {'status': 'invalid_password', 'message': 'Password Incorrect'}, 401

            now = datetime.now()
            expiry_time = now + timedelta(hours=12)
            JWT_SECRET_KEY = current_app.config.get('JWT_SECRET_KEY')
            jwt_payload = {
                'user_id': user.id,
                'email': user.email,
                'iat': now.replace(tzinfo=timezone.utc).timestamp(),
                'exp': expiry_time.replace(tzinfo=timezone.utc).timestamp(),
            }

            jwt_token = jwt.encode(jwt_payload, key=JWT_SECRET_KEY, algorithm='HS256').decode('utf-8')


            return {
                'status': 'ok',
                'jwt_token': jwt_token
            }


        except Exception as ex:
            return {'status': 'error',
                    'message': f'Unexpected Error in {self.__class__.__name__} get',
                    'error': str(ex)}, 500


@swagger.model
class RegisterRequest:
    resource_fields = {
        "email": fields.String,
        "password": fields.String,
        "first_name": fields.String,
        "last_name": fields.String,
    }
    required = ["email", "password"]


class Register(Resource):
    @swagger.operation(
        parameters=[
            {
                "dataType": RegisterRequest.__name__,
                "name": "payload", "required": True, "allowMultiple": False, "paramType": "body",
            }
        ],
        responseMessages=[
            {"code": 200, "message": "Successful Request"},
            {"code": 400, "message": "Invalid Request"},
            {"code": 500, "message": "Unexpected error"},
        ]
    )
    def post(self):
        """ Creates User """
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, required=True)
            parser.add_argument('password', type=str, required=True)
            parser.add_argument('first_name', type=str, required=False)
            parser.add_argument('last_name', type=str, required=False)
            args = parser.parse_args()
        except Exception as e:
            return {'status': 'invalid_request', 'message': 'Email / password not provided'}, 400
        try:

            email = args.get('email')
            password = args.get('password')
            first_name = args.get('first_name')
            last_name = args.get('last_name')

            email_regex = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.search(email_regex, email):
                return {"status": "invalid_email", "message": "Invalid email"}, 401

            if Users.query.filter(Users.email==email).all():
                return {"status": "invalid_email", "message": "Email already in use"}, 401

            if len(password) < 8:
                return {"status": "invalid_password", "message": "Password must be at least 8 characters"}, 401

            user = Users(
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
            user.set_hashed_password(password)

            db.session.add(user)
            db.session.commit()

            return {'status': 'user_created', 'message': 'User Created'}, 200

        except Exception as ex:
            return {'status': 'error',
                    'message': f'Unexpected Error in {self.__class__.__name__} post',
                    'error': str(ex)}, 500