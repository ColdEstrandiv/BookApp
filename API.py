from data import User, Library, Book, Review, BookProgress, ReadingSession, Admin
from flask import Flask, jsonify, request
from data import get_db
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta

# TODO: Postman script 
# TODO: flask BluePrints
# TODO: json validation
# TODO: gitgnore venv
app = Flask(__name__)

@app.route("/user", methods=["GET", "POST", "DELETE"])
def user():
    db = get_db()
    user = request.json
    match request.method:

        case "GET":
            getUser = db.query(User).where(User.id == int(user["id"])).first()

            if not getUser:
                return "User not found", 200
            
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
            newUser = User(
                firstName=user["firstName"],
                lastName=user["lastName"],
                username=user["username"],
                email=user["email"],
                password=user["password"]
            )

            db.add(newUser)
            try:
                db.commit()
                return f"{newUser.username} added to database", 200
            except IntegrityError:
                db.rollback()
                return "Username or email already in use"
            
        case "DELETE":
            user = request.json
            deletedUser = db.query(User).where(User.id == int(user["id"])).first()

            if not deletedUser:
                return "No user to be deleted"
            
            else:
                db.delete(deletedUser)
                db.commit()
                return f"{deletedUser.username} has been deleted", 200

@app.route("/user/bookProgress")
def get_user_bookProgresses():
    ...

@app.route("/user/reads", methods=["GET", "POST", "DELETE"])
def get_user_reads():
    db = get_db()
    userRead = request.json
    match request.method:
        case "GET":
            getUserRead = db.query(User).where(User.id == int(userRead["id"])).first()
            result = []

            if not getUserRead:
                return "User not found", 200
            
            elif userRead["timeFrame"]  == "week":
                result.append("Reads This week")
                one_week = datetime.now() - timedelta(days=7)

                for bP in sorted(getUserRead.bookProgresses, key=lambda b: b.status):
                    result.append(f"{bP.status} {bP.book.title}")
                    for r in sorted(bP.readingSessions, reverse=True, key=lambda d: d.dateMade):
                        if r.dateMade >= one_week:
                            result.append(f"SessionIDRead {r.pageCount} pages on {r.dateMade}")
            
            elif userRead["timeFrame"] == "all":
                result.append("All Reads")
                
                for bP in sorted(getUserRead.bookProgresses, key=lambda b: b.status):
                    result.append(f"{bP.status} {bP.book.title}")
                    for r in sorted(bP.readingSessions, reverse=True, key=lambda d: d.dateMade):
                        result.append(f"Read {r.pageCount} pages on {r.dateMade}")

            return jsonify(result), 200
        
        case "POST":
            getBookProgress = db.query(BookProgress).where(BookProgress.id == int(userRead["id"])).first()
            timeObject = datetime.strptime(userRead["readTime"], "%H:%M").time()

            if not getBookProgress:
                return "BookProgress not found", 200
            
            else:
                newReadSession = ReadingSession(
                bookProgress = getBookProgress,
                pageCount = int(userRead["pageCount"]),
                readTime = timeObject
            )
                db.add(newReadSession)
                db.commit()

        case "DELETE":  
            deletedRead = db.query(ReadingSession).where(ReadingSession.id == int(userRead["id"])).first()

            if not deletedRead:
                return "No read to be deleted", 200
            
            else:
                db.delete(deletedRead)
                db.commit()
                return f"Read id: {deletedRead.id} deleted", 200

@app.route("/libraries/<userId>")
def get_libraries_by_user():
    ...

@app.route("/library/<libraryId>")
def get_library_by_id():
    ...

@app.route("/book/<bookId>")
def get_book():
    # Show Book data, users reading book
    ...


@app.route("/readings")
def get_user_book_reads():
    ...

@app.route("/reviews")
def leave_review():
    ...

# TODO: intergrate (https://openlibrary.org/developers/api)
@app.route("/admin")
def admin_add_book():
    ...

if __name__ == "__main__":
    app.run(port=5000, debug=True)
