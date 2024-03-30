from flask import Blueprint, request, jsonify
from data import get_db
from data import Review

getReviewById = Blueprint('getReviewById', __name__, template_folder='blueprints')

@getReviewById.route("/review/<id>", methods=["GET", "DELETE"])
def review_by_id(id):
    db = get_db()

    match request.method:
        case "GET":
            getReview = db.query(Review).where(Review.id == int(id)).first()

            if not getReview:
                return "Review not found", 404
            
            result = {
                "id": getReview.id,
                "user": getReview.user.username,
                "book": f"{getReview.book.title} by {getReview.book.author}",
                "pageCount": getReview.book.pageCount,
                "content": getReview.content
            }

            return jsonify(result), 200
        
        case "DELETE":
            deletedReview = db.query(Review).where(Review.id == int(id)).first()

            if not deletedReview:
                return "No review for deletion", 404
            
            db.delete(deletedReview)
            db.commit()
            return "Review deleted", 200