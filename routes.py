from flask import Blueprint, request, jsonify, render_template
from models import db, Client, Book

app = Blueprint('routes', __name__)

@app.route('/')
def index():
    return render_template('index.html')


# Clients
@app.route('/clients', methods=['GET', 'POST'])
def handle_clients():
    if request.method == 'GET':
        clients = Client.query.all()
        return render_template('clients.html', clients=clients)
    elif request.method == 'POST':
        data = request.get_json()
        new_client = Client(name=data['name'])
        db.session.add(new_client)
        db.session.commit()
        return jsonify({'id': new_client.id, 'name': new_client.name}), 201

@app.route('/clients/<int:id>', methods=['GET', 'DELETE'])
def handle_client(id):
    client = Client.query.get(id)
    if client:
        if request.method == 'GET':
            return jsonify({'id': client.id, 'name': client.name})
        elif request.method == 'DELETE':
            db.session.delete(client)
            db.session.commit()
            return '', 204
    return '', 404

# Borrow
@app.route('/borrow', methods=['POST'])
def borrow_book():
    data = request.get_json()
    client_id = data.get('client_id')
    book_id = data.get('book_id')

    if not client_id or not book_id:
        return jsonify({'error': 'Client ID and Book ID are required'}), 400

    client = Client.query.get(client_id)
    book = Book.query.get(book_id)

    if not client or not book:
        return jsonify({'error': 'Client or Book not found'}), 404

    if not book.available:
        return jsonify({'error': 'Book is already borrowed'}), 400

    book.available = False
    db.session.commit()
    return jsonify({'message': f'Book "{book.title}" borrowed by client "{client.name}"'}), 200

@app.route('/return', methods=['POST'])
def return_book():
    data = request.get_json()
    client_id = data.get('client_id')
    book_id = data.get('book_id')

    if not client_id or not book_id:
        return jsonify({'error': 'Client ID and Book ID are required'}), 400
    book = Book.query.get(book_id)
    if book.available:
        return jsonify({'error': 'Book is not borrowed'}), 400
    book.available = True
    db.session.commit()
    return jsonify({'message': f'Book "{book.title}" returned'}), 200

# Books
@app.route('/books', methods=['GET', 'POST'])
def handle_books():
    if request.method == 'GET':
        books=Book.query.all()
        return render_template('books.html', books=books)
    elif request.method == 'POST':
        data = request.get_json()
        new_book = Book(title=data['title'], author=data['author'], available=data.get('available', True))
        db.session.add(new_book)
        db.session.commit()
        return jsonify({'id': new_book.id, 'title': new_book.title, 'author': new_book.author, 'available': new_book.available}), 201

@app.route('/books/<int:id>', methods=['GET', 'DELETE'])
def handle_book(id):
    book = Book.query.get(id)
    if book:
        if request.method == 'GET':
            return jsonify({'id': book.id, 'title': book.title, 'author': book.author, 'available': book.available})
        elif request.method == 'DELETE':
            db.session.delete(book)
            db.session.commit()
            return '', 204
    return '', 404
    