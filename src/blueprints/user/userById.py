from flask import Blueprint, request, jsonify
from data import get_db
from data import User

userById = Blueprint('userById', __name__, template_folder='blueprints')

@userById.route("/user/<id>", methods=["GET", "DELETE"])
def user_by_id(id):
    db = get_db()

    match request.method:
        case "GET":
            getUser = db.query(User).where(User.id == int(id)).first()
            
            if not getUser:
                return "User not found", 422
            
            result = {
                "id": getUser.id,
                "firstName": getUser.firstName,
                "lastName": getUser.lastName,
                "username": getUser.username,
                "email": getUser.email,
                "password": getUser.password,
                "admin": getUser.admin
            }
            return jsonify(result), 200
        
        case"DELETE":
            deletedUser = db.query(User).where(User.id == int(id)).first()
            if not deletedUser:
                    return "No user to be deleted", 404
                
            db.delete(deletedUser)
            db.commit()
            return f"{deletedUser.username} has been deleted", 200           