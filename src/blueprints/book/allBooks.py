from flask import Blueprint, jsonify
from data import get_db
from data import Book

getAllBooks = Blueprint('getAllBooks', __name__, template_folder='blueprints')

@getAllBooks.route("/books", methods=["GET"])
def get_all_books():
    db = get_db()
    allBooks = db.query(Book).all()

    result = [{
        "id": b.id,
        "title": b.title,
        "author": b.author,
        "pageCount": b.pageCount
    }
    for b in allBooks]

    return jsonify(result), 200