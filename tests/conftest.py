import pytest
from app import create_app, db 
from flask_jwt_extended import create_access_token

@pytest.fixture
def app():
    app= create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Use an
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": "test_secret"
    })

    with app.app_context():
        db.create_all()
        yield app   
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def access_token(app):
    with app.app_context():
        token = create_access_token(identity={"id": 1})
        return token