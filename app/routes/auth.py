from flask import request
from flask_restx import Namespace, Resource, fields
from app.models import User
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.schema import UserSchema

auth_ns = Namespace('auth', description='Authentication operations')

@auth_ns.route('/test')
class AuthTest(Resource):
    def get(self):
        return {'message': 'Authentication service is running'}, 200

#Swagger models
register_model = auth_ns.model('Register', {
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
})

login_model = auth_ns.model('Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
})

user_schema = UserSchema()
@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_model)
    def post(self):
        data = request.json
        if User.query.filter_by(email=data['email']).first():
            return {'message': 'Email already exists'}, 400
        
        
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        
        return user_schema.dump(user), 201
    
@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.json
        user = User.query.filter_by(email=data['email']).first()
        
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity={'id': user.id, 'username': user.username})
            return {'access_token': access_token}, 200
        
        return {'message': 'Invalid credentials'}, 401
    
@auth_ns.route('/profile')
class Profile(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.get(current_user['id'])
        
        return user_schema.dump(user), 200
    
    @jwt_required()
    def put(self):
        current_user = get_jwt_identity()
        user = User.query.get(current_user['id'])
        
        data = request.json
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.set_password(data['password'])
        
        db.session.commit()
        
        return user_schema.dump(user), 200