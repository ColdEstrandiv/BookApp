from flask import Blueprint, request, jsonify
from data import get_db
from data import User

userById = Blueprint('userById', __name__, template_folder='blueprints')

@userById.route("/user/<id>", methods=["GET", "DELETE", "PUT"])
def user_by_id(id):
    db = get_db()
    getUser = db.query(User).where(User.id == int(id)).first()

    if not getUser:
        return "User not found", 422

    match request.method:
        case "GET":
                        
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
                
            db.delete(getUser)
            db.commit()
            return jsonify(f"{getUser.username} has been deleted", 200)

        case"PUT":
            if getUser.admin == False:
                getUser.admin = True
                db.commit()
                return f"{getUser.username} made admin", 200
            
            else:
                getUser.admin = False
                db.commit()
                return f"{getUser.username} admin revoked", 200