from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restx import Api

db = SQLAlchemy()
jwt = JWTManager()

# Add Swagger security config for JWT
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'JWT Authorization header using the Bearer scheme. Example: "Bearer <your_token>"'
    }
}

api = Api(
    title='Task Manager API',
    version='1.0',
    description='Manage tasks with authentication',
    authorizations=authorizations,
    security='Bearer Auth'
)

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    jwt.init_app(app)
    api.init_app(app)

    # Import and register namespaces
    from app.routes.auth import auth_ns
    from app.routes.tasks import tasks_ns

    api.add_namespace(auth_ns)
    api.add_namespace(tasks_ns)

    return app
