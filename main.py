# main.py
from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)
app.config["DEBUG"] = True

# Lista para almacenar libros (simulando una "base de datos" en memoria)
books_db = [
    {
        "ISBN": "cafc1f20-7eac-477d-9077-261ca83c0bd7",
        "title": "Libro Ejemplo",
        "author": "Autor Ejemplo",
        "quantity": 1,
        "price": 99.99,
        "genre": "Ficción"
    }
]

@app.route('/', methods=['GET'])
def status():
    return jsonify({
        "status": "ok"
    }), 200

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books_db), 200

@app.route('/books', methods=['POST'])
def create_book():
    new_book = request.json
    new_book['ISBN'] = str(uuid.uuid4())
    books_db.append(new_book)
    return jsonify(new_book), 201

@app.route('/books/<ISBN>', methods=['GET'])
def get_book_by_id(ISBN):
    for book in books_db:
        print("eval", book['ISBN'], ISBN)
        if book['ISBN'] == ISBN:
            return jsonify(book), 200
    return jsonify({'message': 'Book not found'}), 404

@app.route('/books/<ISBN>', methods=['PUT'])
def update_book(ISBN):
    updated_data = request.json
    for book in books_db:
        if book['ISBN'] == ISBN:
            book.update(updated_data)
            return jsonify(book)
    return jsonify({'message': 'Book not found'}), 404

@app.route('/books/<ISBN>', methods=['DELETE'])
def delete_book(ISBN):
    for index, book in enumerate(books_db):
        if book['ISBN'] == ISBN:
            del books_db[index]
            return jsonify({'message': 'Book deleted'})
    return jsonify({'message': 'Book not found'}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3030)
