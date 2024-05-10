from flask import Blueprint, request
from data import get_db
from data import Library, User
from marshSchema import CreateLibraryJsonValidation

creatNewLibrary = Blueprint('createNewLibrary', __name__, template_folder='blueprints')

@creatNewLibrary.route("/user/<id>/library", methods=["POST"])
def create_library(id):
    db = get_db()
    getLibrary = request.json
    createLibraryValidation = CreateLibraryJsonValidation()
    createLibraryValidationError = createLibraryValidation.validate(getLibrary)

    if createLibraryValidationError:
        return createLibraryValidationError, 422
    
    getUser = db.query(User).where(User.id == int(id)).first()

    if not getUser:
        return "User not found", 404
    
    newLibrary = Library(name=getLibrary["name"], user=getUser)

    db.add(newLibrary)
    db.commit()
    return f"{newLibrary.name} created for {getUser.username}", 200