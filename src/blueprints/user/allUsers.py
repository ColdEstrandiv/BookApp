from flask import Blueprint, jsonify
from data import get_db
from data import User

getAllusers = Blueprint('getAllusers', __name__, template_folder='blueprints')

@getAllusers.route("/users", methods=["GET"])
def get_all_users():
    db = get_db()
    allUsers = db.query(User).all()

    result = [{
        "id": u.id,
        "firstName": u.firstName,
        "lastName": u.lastName,
        "username": u.username,
        "email": u.email,
        "admin": u.admin
        }
        for u in allUsers]

    return jsonify(result), 200
