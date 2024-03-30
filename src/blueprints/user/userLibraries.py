from flask import Blueprint, jsonify
from data import get_db
from data import User

getUserLibraries = Blueprint('getUserLibraries', __name__, template_folder='blueprints')

@getUserLibraries.route("/user/<id>/libraries", methods=["GET"])
def get_user_libraries(id):
    db = get_db()

    getUser = db.query(User).where(User.id == int(id)).first()
    
    if not getUser:
        return "User not found", 404

    libraries = [
        {
        "id": l.id,
        "name": l.name,
        "books": len(l.books)
        }
        for l in sorted(getUser.libraries, key=lambda n: n.name)
        ]

    return jsonify(libraries), 200