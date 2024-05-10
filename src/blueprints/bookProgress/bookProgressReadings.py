from flask import Blueprint, jsonify
from data import get_db
from data import BookProgress

getBookProgressReadings = Blueprint('getBookProgress', __name__, template_folder='blueprints')

@getBookProgressReadings.route("/bookProgress/<id>/readings", methods=["GET"])
def get_bookProgressReadings(id):
    db = get_db()

    getBookProgress = db.query(BookProgress).where(BookProgress.id == int(id)).first()

    if not getBookProgress:
        return "User not found", 404
    
    readings = [
        {
        "id": r.id,
        "pageCount": r.pageCount,
        "dateMade": r.dateMade,
        "readTime": str (r.readTime)
        }
        for r in sorted(getBookProgress.readingSessions, key=lambda d: d.dateMade)
        ]
    
    return jsonify(readings), 200