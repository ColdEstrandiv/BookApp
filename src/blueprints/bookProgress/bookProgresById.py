from flask import Blueprint, request, jsonify
from data import get_db
from data import BookProgress

bookProgressById = Blueprint('bookProgressById', __name__, template_folder='blueprints')

@bookProgressById.route("/bookProgress/<id>", methods=["GET", "DELETE"])
def book_progress_by_id(id):
    db = get_db()

    match request.method:
        case "GET":
            getBookProgress = db.query(BookProgress).where(BookProgress.id == int(id)).first()

            if not getBookProgress:
                return "Book Progress not found", 404
            
            result ={
                "id": getBookProgress.id,
                "user": getBookProgress.user.username,
                "book": getBookProgress.book.title,
                "status": getBookProgress.status,
            }

            return jsonify(result)
        
        case "DELETE":
            deletedBookProgress = db.query(BookProgress).where(BookProgress.id == int(id)).first()

            if not getBookProgress:
                return "No progress to delete", 404

            dbpUser = deletedBookProgress.user
            dbpBook = deletedBookProgress.book

            db.delete(deletedBookProgress)
            db.commit()
            return f"Bookprogress for {dbpBook.title} by {dbpUser.username} has been deleted", 200    