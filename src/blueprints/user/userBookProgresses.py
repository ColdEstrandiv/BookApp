from flask import Blueprint, jsonify
from data import get_db
from data import User

getUserBookProgresses = Blueprint('getUserBookProgresses', __name__, template_folder='blueprints')

@getUserBookProgresses.route("/user/<id>/bookProgresses", methods=["GET"])
def get_user_book_progresses(id):
    db = get_db()

    getUser = db.query(User).where(User.id == int(id)).first()
    
    if not getUser:
        return "User not found", 404

    bookProgresses = [
        {
        "id": b.id,
        "book": f'{b.book.title} by {b.book.author}',
        "status": b.status,
        "reads": len(b.readingSessions)
        }
        for b in sorted(getUser.bookProgresses, key=lambda s: s.status)
        ]

    return jsonify(bookProgresses), 200