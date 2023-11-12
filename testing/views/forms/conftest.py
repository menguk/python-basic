from flask.testing import FlaskClient
from pytest import fixture
from app import app #импортируем само приложение

@fixture
def client() -> FlaskClient:
    with app.test_client() as test_client:
        with app.app_context():
            yield test_client
