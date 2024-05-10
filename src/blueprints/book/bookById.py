from flask import Blueprint, request, jsonify
from data import get_db, Book

getBookbyId = Blueprint('getBookbyId', __name__, template_folder='blueprints')

@getBookbyId.route("/book/<id>", methods=["GET", "DELETE"])
def get_book_by_id(id):
    db = get_db()

    match request.method:
        case "GET":
            getBook = db.query(Book).where(Book.id == int(id)).first()

            if not getBook:
                return "Book not found", 404
            
            result = {
                "id": getBook.id,
                "title": getBook.title,
                "author": getBook.author,
                "pageCount": getBook.pageCount
            }

            return jsonify(result), 200
            
            
        case "DELETE":
            deletedBook = db.query(Book).where(Book.id == int(id)).first()

            if not deletedBook:
                return "No book to be deleted", 404
            
            db.delete(deletedBook)
            db.commit()
            return f"{deletedBook.title} by {deletedBook.author} has been deleted"