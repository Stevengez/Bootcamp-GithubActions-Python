import pytest
from main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_status(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'ok'

def test_get_books(client):
    response = client.get('/books')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_create_book(client):
    new_book = {
        "title": "Nuevo Libro",
        "author": "Autor Nuevo",
        "quantity": 1,
        "price": 99.99,
        "genre": "Ficción"
    }
    response = client.post('/books', json=new_book)
    assert response.status_code == 201
    assert 'ISBN' in response.get_json()

def test_get_book_by_id(client):
    isbn = 'cafc1f20-7eac-477d-9077-261ca83c0bd7'
    response = client.get('/books/cafc1f20-7eac-477d-9077-261ca83c0bd7')
    assert response.status_code == 200
    assert response.get_json()['ISBN'] == isbn

def test_update_book(client):
    isbn = 'cafc1f20-7eac-477d-9077-261ca83c0bd7'
    updated_data = {
        "title": "Libro Actualizado",
        "author": "Autor Actualizado",
        "quantity": 2,
        "price": 150.00,
        "genre": "Fantasía"
    }
    response = client.put('/books/cafc1f20-7eac-477d-9077-261ca83c0bd7', json=updated_data)
    assert response.status_code == 200
    assert response.get_json()['ISBN'] == isbn

def test_delete_book(client):
    isbn = 'cafc1f20-7eac-477d-9077-261ca83c0bd7'
    response = client.delete('/books/cafc1f20-7eac-477d-9077-261ca83c0bd7')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Book deleted'

def test_delete_book_failure(client):
    isbn = 'isbn-inexistente'
    response = client.delete('/books/{isbn}')
    assert response.status_code == 404
#     assert response.get_json()['message'] == 'Book not found'
