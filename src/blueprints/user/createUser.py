from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from data import get_db
from data import User
from marshSchema import CreateUserJsonValidation

createNewUser = Blueprint('createNewUser', __name__, template_folder='blueprints')

@createNewUser.route("/user", methods=["POST"])
def create_user():
    db = get_db()
    newUser = request.json
    createUserValidation = CreateUserJsonValidation()
    createUserJsonValidationError = createUserValidation.validate(newUser)

    if createUserJsonValidationError:
        return createUserJsonValidationError, 422
    
    newUser = User(
        firstName=newUser["firstName"],
        lastName=newUser["lastName"],
        username=newUser["username"],
        email=newUser["email"],
        password=newUser["password"]
    )
    
    try:
        db.add(newUser)
        db.commit()
        return f"{newUser.username} added to database", 200
    except IntegrityError:
        db.rollback()
        return "Username or email already in use"