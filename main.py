from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:password123@192.168.0.49/bootcampdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__ = 'book'

    ISBN = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    author = db.Column(db.String)
    title = db.Column(db.String)
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    genre = db.Column(db.String)

    def __init__(self, title, author, ISBN=None, genre=None, price=None, quantity=None):
        self.title = title
        self.author = author
        self.ISBN = ISBN if ISBN else str(uuid.uuid4())
        self.price = price
        self.quantity = quantity
        self.genre = genre
    
    def __repr__(self):
        return f'<Book {self.title}>'
    
    def to_dict(self):
        return {
            'ISBN': self.ISBN,
            'author': self.author,
            'title': self.title,
            'price': self.price,
            'quantity': self.quantity,
            'genre': self.genre
        }

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def get_author(self):
        return self.author

    def set_author(self, author):
        self.author = author

    def get_ISBN(self):
        return self.ISBN

    def set_ISBN(self, ISBN):
        self.ISBN = ISBN

    def get_price(self):
        return self.price

    def set_price(self, price):
        self.price = price

    def get_quantity(self):
        return self.quantity

    def set_quantity(self, quantity):
        self.quantity = quantity

    def get_genre(self):
        return self.genre

    def set_genre(self, genre):
        self.genre = genre

class BookService:

    @staticmethod
    def get_books():
        return Book.query.all()

    @staticmethod
    def save_book(book_data):
        new_book = Book(
            title=book_data['title'],
            author=book_data['author'],
            genre=book_data.get('genre'),
            price=book_data.get('price'),
            quantity=book_data.get('quantity')
        )
        db.session.add(new_book)
        db.session.commit()
        return new_book

    @staticmethod
    def get_by_id(ISBN):
        return Book.query.get(ISBN)

    @staticmethod
    def update_by_id(book_data, ISBN):
        book = Book.query.get(ISBN)
        if book:
            book.author = book_data.get('author', book.author)
            book.price = book_data.get('price', book.price)
            book.quantity = book_data.get('quantity', book.quantity)
            book.title = book_data.get('title', book.title)
            book.genre = book_data.get('genre', book.genre)
            db.session.commit()
            return book
        return None

    @staticmethod
    def delete_by_id(ISBN):
        book = Book.query.get(ISBN)
        if book:
            db.session.delete(book)
            db.session.commit()
            return True
        return False

@app.route('/', methods=['GET'])
def status():
    return jsonify({
        "status": "ok"
    }), 200

@app.route('/books', methods=['GET'])
def get_books():
    books = BookService.get_books()
    return jsonify([book.to_dict() for book in books]), 200

@app.route('/books', methods=['POST'])
def create_book():
    book_data = request.json
    book = BookService.save_book(book_data)
    print("CP0", book.to_dict())
    return jsonify(book.to_dict()), 201

@app.route('/books/<ISBN>', methods=['GET'])
def get_book_by_id(ISBN):
    book = BookService.get_by_id(ISBN)
    if book:
        return jsonify(book.to_dict())
    return jsonify({'message': 'Book not found'}), 404

@app.route('/books/<ISBN>', methods=['PUT'])
def update_book(ISBN):
    book_data = request.json
    book = BookService.update_by_id(book_data, ISBN)
    if book:
        return jsonify(book.to_dict())
    return jsonify({'message': 'Book not found'}), 404

@app.route('/books/<ISBN>', methods=['DELETE'])
def delete_book(ISBN):
    success = BookService.delete_by_id(ISBN)
    if success:
        return jsonify({'message': 'Book deleted'})
    return jsonify({'message': 'Book not found'}), 404

app.run(host='0.0.0.0', port=3030)