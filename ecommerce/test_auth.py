import pytest

from app import create_app

@pytest.fixture

def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_register(client):
    response = client.post('/register', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    assert response.status_code == 201

def test_register_invalid(client):
    response = client.post('/register', json={
        'email': 'test@example.com',
    })
    assert response.status_code == 400
    response = client.post('/register', json={
        'password': 'test123'
    })
    assert response.status_code == 400
    response = client.post('/register', json={
    })
    assert response.status_code == 400

def test_login_after_register(client):
    client.post('/register', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    response = client.post('/login', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    assert response.status_code == 200

def test_invalid_login(client):
    response = client.post('/login', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    assert response.status_code == 401

def test_logout_after_login(client):
    client.post('/register', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    client.post('/login', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    response = client.post('/logout', json={
    })
    assert response.status_code == 200