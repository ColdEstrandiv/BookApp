from flask import Blueprint, jsonify
from data import get_db
from data import Library, Book

getBooksNotInLibrary = Blueprint('getBooksNotInLibrary', __name__, template_folder='blueprints')

@getBooksNotInLibrary.route("/library/<id>/otherBooks", methods=["GET"])
def get_all_books(id):
    db = get_db()

    getLibrary = db.query(Library).where(Library.id == int(id)).first()

    if not getLibrary:
        return "Library not found", 404
    

    if getLibrary.books:
        allOtherBooks = db.query(Book).filter(~Book.libraries.any(Library.id == int(id)))

        result = [{
            "id": b.id,
            "title": b.title,
            "author": b.author,
            "pageCount": b.pageCount
        }
        for b in sorted(allOtherBooks, key=lambda b: b.title)]

        return jsonify(result), 200
    
    else:
        allBooks = db.query(Book).all()

        result = [{
            "id": b.id,
            "title": b.title,
            "author": b.author,
            "pageCount": b.pageCount
        }
        for b in allBooks]

        return jsonify(result), 200