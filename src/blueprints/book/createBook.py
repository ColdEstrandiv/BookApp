from flask import Blueprint, request
from data import get_db, Book
from marshSchema import CreateBookJsonValidation

createNewBook = Blueprint('createNewBook', __name__, template_folder='blueprints')

@createNewBook.route("/book", methods=["POST"])
def create_book():
    db = get_db()
    getBook = request.json
    createBookValidation = CreateBookJsonValidation()
    createBookValidationError = createBookValidation.validate(getBook)

    if createBookValidationError:
        return createBookValidationError, 422
    
    newBook = Book(title=getBook["title"],
                author=getBook["author"],
                pageCount=getBook["pageCount"]
                )
   
    db.add(newBook)
    db.commit()
    return f"{newBook.title} by {newBook.author} has been added to database"    
