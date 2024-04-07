from flask import Blueprint, request, jsonify
from data import get_db
from data import Library

getAllLibraryBooks = Blueprint('getAllLibraryBooks', __name__, template_folder='blueprints')

@getAllLibraryBooks.route("/library/<id>/books", methods=["GET"])
def library_Books(id):
    db = get_db()

    match request.method:
        case "GET":
            getLibrary = db.query(Library).where(Library.id == int(id)).first()

            if not getLibrary:
                return "Library not found", 404
            
            if len(getLibrary.books) > 0:
                result = [
                    {
                    "id": b.id,
                    "title": b.title,
                    "author": b.author,
                    "pageCount": b.pageCount
                    }
                    for b in sorted(getLibrary.books, key=lambda b: b.author)
                    ]
                return jsonify(result), 200
            
            return None, 200
        