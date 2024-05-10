from flask import Blueprint, request, jsonify
from data import get_db
from data import User
from marshSchema import UserReadJsonValidation
from datetime import datetime, timedelta

userReadsById = Blueprint('userReadsById', __name__, template_folder='blueprints')

@userReadsById.route("/user/<id>/reads", methods=['GET'])
def get_user_reads(id):
    db = get_db()
    timeFrame = request.json
    userReadValidation = UserReadJsonValidation()
    userReadValidationError = userReadValidation.validate(timeFrame)
    result = []

    if userReadValidationError:
        return userReadValidationError, 422
    
    getUser = db.query(User).where(User.id == int(id)).first()

    if not getUser:
        return "User not found", 404
    
    if timeFrame["timeFrame"]  == "week":
        result.append("Reads past week")
        oneWeek = datetime.now() - timedelta(days=7)

        for bP in sorted(getUser.bookProgresses, key=lambda b: b.status):
            result.append(f"{bP.status} {bP.book.title}")
            for r in sorted(bP.readingSessions, reverse=True, key=lambda d: d.dateMade):
                if r.dateMade >= oneWeek:
                    result.append(f"SessionID: {r.id}, Read {r.pageCount} pages on {r.dateMade}")
    
    if timeFrame["timeFrame"] == "month":
        result.append("Reads past month")
        oneMonth = datetime.now() - timedelta(days=30)

        for bP in sorted(getUser.bookProgresses, key=lambda b: b.status):
            result.append(f"{bP.status} {bP.book.title}")
            for r in sorted(bP.readingSessions, reverse=True, key=lambda d: d.dateMade):
                if r.dateMade >= oneMonth:
                    result.append(f"SessionID: {r.id}, Read {r.pageCount} pages on {r.dateMade}")

    if timeFrame["timeFrame"] == "all":
        result.append("All Reads")
        
        for bP in sorted(getUser.bookProgresses, key=lambda b: b.status):
            result.append(f"{bP.status} {bP.book.title}")
            for r in sorted(bP.readingSessions, reverse=True, key=lambda d: d.dateMade):
                result.append(f"SessionID: {r.id}, Read {r.pageCount} pages on {r.dateMade}")

    return jsonify(result), 200
