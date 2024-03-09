from flask import Blueprint
from data import get_db
from data import BookProgress, User, Book

createBookProgress = Blueprint('createBookProgress', __name__, template_folder='blueprints')

@createBookProgress.route("/user/<uId>/bookProgress/book/<bId>", methods=["POST"])
def create_book_progress(uId, bId):
    db = get_db()

    getUser = db.query(User).where(User.id == int(uId)).first()
    getBook = db.query(Book).where(Book.id == int(bId)).first()

    if not getUser:
        return "User not found", 404
    if not getBook:
        return "Book not found", 404
    
    newBookProgress = BookProgress(user=getUser, book=getBook)

    db.add(newBookProgress)
    db.commit()
    return f"Bookprogress for {getBook.title} by {getUser.username} created", 200