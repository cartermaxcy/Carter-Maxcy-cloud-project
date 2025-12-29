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

def test_get_empty_products(client):
    response = client.get('/products', json={
    })
    assert response.status_code == 200
    assert response.data == b'[]\n'

def test_create_without_login_fails(client):
    response = client.post('/products', json={
        'name': 'test name',
        'description' : 'test description',
        'price': .99,
        'stock': 'test stock',
        'image_url': 'test.url'
    })
    assert response.status_code == 401

def test_create_product(client):
    client.post('/register', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    client.post('/login', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    response = client.post('/products', json={
        'name': 'test name',
        'description' : 'test description',
        'price': .99,
        'stock': 'test stock',
        'image_url': 'test.url'
    })
    assert response.status_code == 201

def test_update_product(client):
    client.post('/register', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    client.post('/login', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    client.post('/products', json={
        'name': 'test name',
        'description' : 'test description',
        'price': .99,
        'stock': 'test stock',
        'image_url': 'test.url'
    })
    response = client.put('/products/1', json={
        'name': 'test name',
        'description' : 'test description',
        'price': .99,
        'stock': 'test stock',
        'image_url': 'test.url'
    })
    assert response.status_code == 200

def test_delete_product(client):
    client.post('/register', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    client.post('/login', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    client.post('/products', json={
        'name': 'test name',
        'description' : 'test description',
        'price': .99,
        'stock': 'test stock',
        'image_url': 'test.url'
    })
    response = client.delete('/products/1', json={
        'name': 'test name',
        'description' : 'test description',
        'price': .99,
        'stock': 'test stock',
        'image_url': 'test.url'
    })
    assert response.status_code == 200

    # Check there are no more products.
    response = client.get('/products', json={
    })
    assert response.status_code == 200
    assert response.data == b'[]\n'