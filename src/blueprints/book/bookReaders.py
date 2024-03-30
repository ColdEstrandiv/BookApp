from flask import Blueprint, jsonify
from data import get_db
from data import Book

getBookReaders = Blueprint('getBookReaders', __name__, template_folder='blueprints')

@getBookReaders.route("/book/<id>/readers", methods=["GET"])
def book_readers(id):
    db = get_db()

    getBook = db.query(Book).where(Book.id == int(id)).first()

    if not getBook:
        return "Book not found", 404
    
    result = [(b.user.firstName, b.user.lastName) for b in sorted(getBook.bookProgresses)]

    return jsonify(result), 200
