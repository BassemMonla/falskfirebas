from flask import Flask
from models import db, Client, Book
from routes import app as routes_app
import logging  # Import the logging module

# Configure logging (optional, but helpful for debugging)
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db.init_app(app)
app.register_blueprint(routes_app)

@app.cli.command("init_db")  # Define the CLI command
def init_db_command():
    """Creates the database tables and populates them with initial data."""
    with app.app_context():
        db.create_all()

        logging.debug("Clearing existing data from the database...")
        db.session.query(Client).delete()
        db.session.query(Book).delete()
        db.session.commit()
        logging.debug("Database cleared.")

        logging.debug("Adding initial data...")
        client1 = Client(name="Alice")
        client2 = Client(name="Bob")
        db.session.add_all([client1, client2])

        book1 = Book(title="The Lord of the Rings", author="J.R.R. Tolkien")
        book2 = Book(title="Pride and Prejudice", author="Jane Austen")
        book3 = Book(title="1984", author="George Orwell")
        db.session.add_all([book1, book2, book3])

        db.session.commit()
        logging.debug("Initial data added and committed.")
        print("Initialized the database.")


if __name__ == '__main__':
    app.run(debug=True)