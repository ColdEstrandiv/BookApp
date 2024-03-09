from flask import Blueprint, request, jsonify
from data import get_db
from data import User, Book, Review
from marshSchema import CreateReviewJsonValidation

createNewReview = Blueprint('createNewReview', __name__, template_folder='blueprints')

@createNewReview.route("/user/<uId>/book/<bId>/review", methods=["POST"])
def create_review(uId, bId):
    db = get_db()
    getReview = request.json
    createReviewValidation = CreateReviewJsonValidation()
    createReviewValidationError = createReviewValidation.validate(getReview)

    if createReviewValidationError:
        return createReviewValidationError, 422
    
    getUser = db.query(User).where(User.id == int(uId)).first()

    if not getUser:
        return "User not found", 404
    
    getBook = db.query(Book).where(Book.id == int(bId)).first()

    if not getBook:
        return "Book not found", 404
    
    newReview = Review(
        user=getUser,
        book=getBook,
        content=getReview["content"]
    )

    db.add(newReview)
    db.commit()
    return "Review made", 200