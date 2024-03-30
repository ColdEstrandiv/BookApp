from flask import Blueprint
from data import get_db
from data import Library, Book

addLibraryBook = Blueprint('addLibraryBook', __name__, template_folder='blueprint')

@addLibraryBook.route("/library/<lId>/book/<bId>", methods=["PUT"])
def add_book_to_library(lId, bId):
    db = get_db()

    getLibrary = db.query(Library).where(Library.id == int(lId)).first()

    if not getLibrary:
        return "Library not found", 404
    
    getBook = db.query(Book).where(Book.id == int(bId)).first()

    if not getBook:
        return "Book not found", 404
    
    if getBook not in getLibrary.books:
        getLibrary.books.append(getBook)
        db.commit()
        return f"{getBook.title} by {getBook.author} added to {getLibrary.name}", 200
    
    return f"{getBook.title} by {getBook.author} already in {getLibrary.name}", 200