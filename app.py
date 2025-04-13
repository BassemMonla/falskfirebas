from flask import Flask
from models import db, Client, Book
from routes import app as routes_app

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db.init_app(app)
app.register_blueprint(routes_app)  # Register the routes from routes.py

with app.app_context():
    db.create_all()
    
    # Add initial data if the database is empty
    if not db.session.query(Client).first() and not db.session.query(Book).first():
        # Add clients
        client1 = Client(name="Alice")
        client2 = Client(name="Bob")
        db.session.add_all([client1, client2])

        # Add books
        book1 = Book(title="The Lord of the Rings", author="J.R.R. Tolkien")
        book2 = Book(title="Pride and Prejudice", author="Jane Austen")
        book3 = Book(title="1984", author="George Orwell")
        db.session.add_all([book1, book2, book3])

        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)