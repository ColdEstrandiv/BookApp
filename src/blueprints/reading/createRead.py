from flask import Blueprint, request
from data import get_db, ReadingSession, BookProgress
from marshSchema import CreateUserReadJsonValidation
from datetime import datetime

createNewRead = Blueprint('createNewRead', __name__, template_folder='blueprints')

@createNewRead.route("/bookProgress/<id>/read", methods=["POST"])
def create_read(id):
    db = get_db()
    getRead = request.json
    createReadValidation = CreateUserReadJsonValidation()
    createReadValidationError = createReadValidation.validate(getRead)

    if createReadValidationError:
        return createReadValidationError, 422
    
    getBookProgress = db.query(BookProgress).where(BookProgress.id == int(id)).first()
    
    try:
        timeObject = datetime.strptime(getRead["readTime"], "%H:%M").time()
    except ValueError:
        return "Not a valid time please use HH:MM", 422

    if not getBookProgress:
        return "BookProgress not found", 404
    
    else:
        newReadSession = ReadingSession(
            bookProgress = getBookProgress,
            pageCount = int(getRead["pageCount"]),
            readTime = timeObject
        )
        db.add(newReadSession)
        db.commit()
        return "Read Session Created", 200



