from flask import Blueprint, jsonify
from flask_restful import Resource, reqparse, Api
from flask_jwt_extended import create_access_token
from error_handler import InvalidAPIUsage
from extensions import bcrypt
from db import db
from auth.models import User

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

api = Api(auth_blueprint)

parser = reqparse.RequestParser()

parser.add_argument('username', type=str)
parser.add_argument('email', type=str)
parser.add_argument('password', type=str)


@auth_blueprint.errorhandler(InvalidAPIUsage)
def bad_request_400(e):
    return jsonify(e.to_dict()), e.status_code


@auth_blueprint.errorhandler(InvalidAPIUsage)
def unauthorized_401(e):
    return jsonify(e.to_dict()), e.status_code


class UserRegistration(Resource):
    def post(self):
        try:
            args = parser.parse_args()
            required_fields = ['username', 'email', 'password']
            for field in required_fields:
                if not args[field]:
                    raise InvalidAPIUsage(f'{field} is missing')
            hashed_password = bcrypt.generate_password_hash(args['password'])
            new_user = User(username=args['username'], email=args['email'], password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return {"message": "User registered successful", "user": new_user.to_dict()}, 201
        except Exception as e:
            raise e


class UserLogin(Resource):
    def post(self):
        try:
            args = parser.parse_args()
            required_fields = ['email', 'password']
            for field in required_fields:
                if not args[field]:
                    raise InvalidAPIUsage(f'{field} is missing')
            user = User.query.filter_by(email=args['email']).first()
            if not user:
                raise InvalidAPIUsage('User does not exist')
            is_correct_password = bcrypt.check_password_hash(user.password_hash, args['password'])
            if user and is_correct_password:
                access_token = create_access_token(identity=user.id)
                return jsonify(access_token=access_token, user=user.to_dict())
            else:
                raise InvalidAPIUsage('Wrong username or password', 401)
        except Exception as e:
            raise e


api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')


auth_blueprint.register_error_handler(400, bad_request_400)
auth_blueprint.register_error_handler(401, unauthorized_401)
