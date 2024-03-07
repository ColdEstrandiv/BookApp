from flask import Blueprint, request, jsonify, Flask
from sqlalchemy.exc import IntegrityError
from data import get_db
from data import User
from ..marshSchema import CreateUserJsonValidation, IdJsonValidation

userPage = Blueprint('user', __name__, template_folder='blueprints')

@userPage.route("/user", methods=["GET", "POST", "DELETE"])
def user():
    db = get_db()
    user = request.json
    createUserValidation = CreateUserJsonValidation()
    idValidation = IdJsonValidation()
    idValidationError = idValidation.validate(user)

    match request.method:

        case "GET":
            if idValidationError:
                return idValidationError, 422

            else:
                getUser = db.query(User).where(User.id == int(user["id"])).first()
                
                if not getUser:
                    return "User not found", 422
                
                else:
                    result = {
                    "id": getUser.id,
                    "firstName": getUser.firstName,
                    "lastName": getUser.lastName,
                    "username": getUser.username,
                    "email": getUser.email,
                    "password": getUser.password
                }
                    return jsonify(result), 200

        case "POST":
            createUserJsonValidationError = createUserValidation.validate(user)

            if createUserJsonValidationError:
                return createUserJsonValidationError, 422
            
            else:
                newUser = User(
                    firstName=user["firstName"],
                    lastName=user["lastName"],
                    username=user["username"],
                    email=user["email"],
                    password=user["password"]
                )
                
                
                try:
                    db.add(newUser)
                    db.commit()
                    return f"{newUser.username} added to database", 200
                except IntegrityError:
                    db.rollback()
                    return "Username or email already in use"
            
        case "DELETE":
            if idValidation:
                return idValidation, 422
            
            else:
                deletedUser = db.query(User).where(User.id == int(user["id"])).first()

                if not deletedUser:
                    return "No user to be deleted", 404
                
                else:
                    db.delete(deletedUser)
                    db.commit()
                    return f"{deletedUser.username} has been deleted", 200