from flask import Blueprint, jsonify
from data import get_db
from data import User

getUserReviews = Blueprint('getUserReviews', __name__, template_folder='blueprints')

@getUserReviews.route("/user/<id>/reviews", methods=["GET"])
def get_user_reviews(id):
    db = get_db()
    
    getUser = db.query(User).where(User.id == int(id)).first()

    if not getUser:
        return "User not found", 404
    
    reviews = [
        {
        "id": r.id,
        "user": r.user.username,
        "book": f"{r.book.title} by {r.book.author}",
        "content": r.content
        }
        for r in sorted(getUser.reviews, key=lambda b: b.book.title)
        ]
    
    return jsonify(reviews), 200