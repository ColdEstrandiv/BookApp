from flask import Blueprint, request, jsonify
from data import get_db, ReadingSession

getReadById = Blueprint('getReadById', __name__, template_folder='blueprints')

@getReadById.route("/read/<id>", methods=["GET", "DELETE"])
def read_by_id(id):
    db = get_db()

    match request.method:
        case "GET":
            getRead = db.query(ReadingSession).where(ReadingSession.id == int(id)).first()

            if not getRead:
                return "Reading session not found", 404
            
            result = {
                "id": getRead.id,
                "bookProgressId": getRead.bookProgressId,
                "pageCount": getRead.pageCount,
                "dateMade": getRead.dateMade,
                "readTime": str(getRead.readTime)
            }
            
            return jsonify(result), 200

        case "DELETE":
            deletedRead = db.query(ReadingSession).where(ReadingSession.id == int(id)).first()

            if not deletedRead:
                return "Reading session not found", 404
            
            db.delete(deletedRead)
            db.commit()
            return f"Read made on {deletedRead.dateMade} deleted", 200