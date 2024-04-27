import sqlite3
import pytest
import main
from main import app as flask_app
import init_db


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_login(app, client):
    res = client.get('/')
    assert res.status_code == 200


def test_database_init():
    init_db.main()
    connection = sqlite3.connect('database.db')
    assert connection


def test_get_post():
    assert (main.get_post(1))


def test_home(client):
    response = client.get("/home")
    assert response.status_code == 302


def test_create(client):
    response = client.get("/create")
    assert response.status_code == 302
