from flask import Blueprint, request, jsonify
from data import get_db
from data import Library

library = Blueprint('library', __name__, template_folder='blueprints')

@library.route("/library/<id>", methods=["GET", "DELETE"])
def library_by_id(id):
    db = get_db()

    match request.method:
        case "GET":
            getLibrary = db.query(Library).where(Library.id == int(id)).first()

            if not getLibrary:
                return "Library not found", 404
            
            libraryBooks = [(f'{b.title} by {b.author}') for b in sorted(getLibrary.books, key=lambda b: b.author)]
            result = {
                "id": getLibrary.id,
                "name": getLibrary.name,
                "user": getLibrary.user.username,
                "userId": getLibrary.userId,
                "books": libraryBooks
            }           

            return jsonify(result), 200
        
        case "DELETE":
            deletedLibrary = db.query(Library).where(Library.id == int(id)).first()
            
            if not deletedLibrary:
                return "library not found", 404
            
            deletedLibrary.books = []
            
            db.delete(deletedLibrary)
            db.commit()
            return f"{deletedLibrary.name} has been deleted", 200