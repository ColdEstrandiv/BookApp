from data import User, Library, Book, Review, BookProgress, ReadingSession, Admin
from flask import Flask, jsonify, request
from data import get_db
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from marshSchema import IdJsonValidation, CreateUserJsonValidation, UserBookIdJsonValidation 
from marshSchema import UserReadJsonValidation, CreateUserReadJsonValidation, CreateLibraryJsonValidation, LibraryBookIdJsonValidation, CreateBookJsonValidation, CreateReviewJsonValidation

# TODO: Postman script 
# TODO: flask BluePrints

app = Flask(__name__)

@app.route("/user", methods=["GET", "POST", "DELETE"])
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

@app.route("/user/bookProgress", methods=["GET", "POST", "DELETE"])
def get_user_bookProgresses():
    db = get_db()
    userBookProgress = request.json
    idValidation = IdJsonValidation()
    userBookIdValidation = UserBookIdJsonValidation()
    idValidationError = idValidation.validate(userBookProgress)

    match request.method:
        case "GET":
            if idValidationError:
                return idValidationError, 422

            else:
                getUserBookProgess = db.query(BookProgress).where(BookProgress.id == userBookProgress["id"]).first()

                if not getUserBookProgess:
                    return "BookProgress not found", 404
                
                else:
                    result ={
                        "id": getUserBookProgess.id,
                        "user": getUserBookProgess.user.username,
                        "book": getUserBookProgess.book.title,
                        "status": getUserBookProgess.status,
                    }

                    return jsonify(result), 200
        
        case "POST":
            userBookIdValidationError = userBookIdValidation.validate(userBookProgress)

            if userBookIdValidationError:
                return userBookIdValidationError, 422
            
            else:
                getUser = db.query(User).where(User.id == int(userBookProgress["userId"])).first()
                getBook = db.query(Book).where(Book.id == int(userBookProgress["bookId"])).first()
                
                if not getBook or not getUser:
                    return "Book or user not found", 404
                
                else:
                    newBookProgress = BookProgress(
                        user=getUser,
                        book=getBook
                    )

                    db.add(newBookProgress)
                    db.commit()
                    return f"Bookprogress for {getBook.title} by {getUser.username} created", 200
        
        case "DELETE":
            if idValidationError:
                return idValidationError, 422
            
            else:
                deletedBookProgress = db.query(BookProgress).where(BookProgress.id == userBookProgress["id"]).first()
                
                # This is done to properly load the objs in the return fstring TODO: find a better way to load these
                dbpUser = deletedBookProgress.user
                dbpBook = deletedBookProgress.book

                if not deletedBookProgress:
                    return "No progress to delete", 404
                
                else:
                    db.delete(deletedBookProgress)
                    db.commit()
                    return f"Bookprogress for {dbpBook.title} by {dbpUser.username} has been deleted", 200

@app.route("/user/reads", methods=["GET", "POST", "DELETE"])
def get_user_reads():
    db = get_db()
    userRead = request.json
    createUserReadValidation = CreateUserReadJsonValidation()
    idTimeFrameValidation = UserReadJsonValidation()
    idTimeFrameValidationError = UserReadJsonValidation().validate(userRead)

    match request.method:
        case "GET":
            if idTimeFrameValidationError:
                return idValidationError, 422
            
            else:
                getUserReadJsonValidation = db.query(User).where(User.id == int(userRead["id"])).first()
                result = []

                if not getUserReadJsonValidation:
                    return "User not found", 404
                
                elif userRead["timeFrame"]  == "week":
                    result.append("Reads past week")
                    oneWeek = datetime.now() - timedelta(days=7)

                    for bP in sorted(getUserReadJsonValidation.bookProgresses, key=lambda b: b.status):
                        result.append(f"{bP.status} {bP.book.title}")
                        for r in sorted(bP.readingSessions, reverse=True, key=lambda d: d.dateMade):
                            if r.dateMade >= oneWeek:
                                result.append(f"SessionID: {r.id}, Read {r.pageCount} pages on {r.dateMade}")
                
                elif userRead["timeFrame"] == "month":
                    result.append("Reads past month")
                    oneMonth = datetime.now() - timedelta(days=30)

                    for bP in sorted(getUserReadJsonValidation.bookProgresses, key=lambda b: b.status):
                        result.append(f"{bP.status} {bP.book.title}")
                        for r in sorted(bP.readingSessions, reverse=True, key=lambda d: d.dateMade):
                            if r.dateMade >= oneMonth:
                                result.append(f"SessionID: {r.id}, Read {r.pageCount} pages on {r.dateMade}")

                elif userRead["timeFrame"] == "all":
                    result.append("All Reads")
                    
                    for bP in sorted(getUserReadJsonValidation.bookProgresses, key=lambda b: b.status):
                        result.append(f"{bP.status} {bP.book.title}")
                        for r in sorted(bP.readingSessions, reverse=True, key=lambda d: d.dateMade):
                            result.append(f"SessionID: {r.id}, Read {r.pageCount} pages on {r.dateMade}")

                return jsonify(result), 200
        
        case "POST":
            createUserReadValidationError = createUserReadValidation.validate(userRead)

            if createUserReadValidationError:
                return createUserReadValidationError, 422
            
            else:
                getBookProgress = db.query(BookProgress).where(BookProgress.id == int(userRead["id"])).first()

                try:
                    timeObject = datetime.strptime(userRead["readTime"], "%H:%M").time()
                except ValueError:
                    return "Not a valid time please use HH:MM", 422

                if not getBookProgress:
                    return "BookProgress not found", 404
                
                else:
                    newReadSession = ReadingSession(
                    bookProgress = getBookProgress,
                    pageCount = int(userRead["pageCount"]),
                    readTime = timeObject
                )
                    db.add(newReadSession)
                    db.commit()
                    return "Read Session Created", 200

        case "DELETE":
            idValidationError = IdJsonValidation().validate(userRead)

            if idValidationError:
                return idValidationError, 422
            
            else:
                deletedRead = db.query(ReadingSession).where(ReadingSession.id == int(userRead["id"])).first()

                if not deletedRead:
                    return "No read to be deleted", 200
                
                else:
                    db.delete(deletedRead)
                    db.commit()
                    return f"Read id: {deletedRead.id} deleted", 200

@app.route("/user/libraries", methods = ["GET"])
def get_libraries_by_user():
    db = get_db()
    getLibrary = request.json
    idValidation = IdJsonValidation()
    idValidationError = idValidation.validate(getLibrary)

    match request.method:
        case "GET":
            if idValidationError:
                return idValidationError, 422
            
            else:
                user = db.query(User).where(User.id == getLibrary["id"]).first()
                result = []

                if not user:
                    return "User not found", 404

                else:
                    for l in sorted(user.libraries, key=lambda n: n.name):
                        result.append(f"{l.name}, ID: {l.id}")

                    return jsonify(result), 200


@app.route("/library", methods=["GET", "POST", "DELETE", "PUT"])
def get_library_by_id():
    db = get_db()
    getLibrary = request.json
    idValidation = IdJsonValidation()
    createLibraryValidation = CreateLibraryJsonValidation()
    libraryBookValidation = LibraryBookIdJsonValidation()
    idValidationError = idValidation.validate(getLibrary)

    match request.method:
        case "GET":
            if idValidationError:
                return idValidationError, 422
            
            else:
                library = db.query(Library).where(Library.id == int(getLibrary["id"])).first()
                libraryBooks = []

                if not library:
                    return "Library not found", 404

                else:
                    for b in sorted(library.books, key=lambda b: b.author):
                        libraryBooks.append(b.title, b.author)

                    result = {
                        "Id": library.id,
                        "name": library.name,
                        "user": library.user.name,
                        "books": libraryBooks
                    }
                    
                    return jsonify(result), 200
        
        case "POST":
            createLibraryValidationError = createLibraryValidation.validate(getLibrary)
            
            if createLibraryValidationError:
                return createLibraryValidationError, 422
            
            else:
                libraryUser = db.query(User).where(User.id == int(getLibrary["id"])).first()

                if not libraryUser:
                    return "User not found", 404
                
                else:
                    newLibrary = Library(
                        name=getLibrary["name"],
                        user=libraryUser
                    )
                    
                    db.add(newLibrary)
                    db.commit()
                    return jsonify(f"{newLibrary.name} created for {libraryUser.username}"), 200

        case "DELETE":
            if idValidationError:
                return idValidationError, 422
            
            else:
                deletedLibrary = db.query(Library).where(Library.id == int(getLibrary["id"])).first()

                if not deletedLibrary:
                    return "Library not found", 404
                
                else:
                    db.delete(deletedLibrary)
                    db.commit()
                    return jsonify(f"{deletedLibrary.name} has been deleted"), 200
        
        case "PUT":
            libraryBookValidationError = libraryBookValidation.validate(getLibrary)

            if libraryBookValidationError:
                return libraryBookValidationError, 422

            else:
                library = db.query(Library).where(Library.id == int(getLibrary["libraryId"])).first()
                book = db.query(Book).where(Book.id == int(getLibrary["bookId"])).first()

                if not library:
                    return "Library not found", 404
                
                elif not book:
                    return "Book not found", 404
                
                else:
                    library.books.append(book)
                    db.commit()
                    return f"{book.title} by {book.author} added to {library.name}", 200
                       
@app.route("/book", methods=["GET", "POST", "DELETE"])
def get_book():
    db = get_db()
    getBook = request.json
    idValidation = IdJsonValidation()
    createBookValidation = CreateBookJsonValidation()
    idValidationError = idValidation.validate(getBook)

    match request.method:
        case "GET":
            if idValidationError:
                return idValidationError, 422
            
            else:
                book = db.query(Book).where(Book.id == int(getBook["id"])).first()

                if not book:
                    return "Book not found", 404
                
                else:
                    result = {
                        "id": book.id,
                        "title": book.title,
                        "author": book.author,
                        "pageCount": book.pageCount
                    }

                    return jsonify(result), 200


        case "POST":
            createBookValidationError = createBookValidation.validate(getBook)

            if createBookValidationError:
                return createBookValidationError, 422
            
            else:
                newBook = Book(title=getBook["title"],
                            author=getBook["author"],
                            pageCount=getBook["pageCount"]
                            )

                db.add(newBook)
                db.commit()

                return f"{newBook.title} by {newBook.author} has been added to database"
        
        case "DELETE":
            if idValidationError:
                return idValidationError, 422
            
            else:
                deletedBook = db.query(Book).where(Book.id == int(getBook["id"])).first()

                if not deletedBook:
                    return "Book not found", 200
                
                else:
                    db.delete(deletedBook)
                    db.commit()
                    return f"{deletedBook.title} by {deletedBook.author} has been deleted"

@app.route("/book/readers", methods=["GET"])
def get_user_book_reads():
    db = get_db()
    getBook = request.json
    idValidation = IdJsonValidation()
    idValidationError = idValidation.validate(getBook)

    if request.method == "GET":
        if idValidationError:
            return idValidationError, 422
        
        else:
            book = db.query(Book).where(Book.id == getBook["id"]).first()
            result = ["Being read by:"]

            for bP in sorted(book.bookProgresses):
                result.append(f"{bP.user.firstName} {bP.user.lastName}")
            
            return jsonify(result), 200


@app.route("/review", methods=["GET", "POST", "DELETE"])
def leave_review():
    db = get_db()
    getReview = request.json
    idValidation = IdJsonValidation()
    createReviewValidation = CreateReviewJsonValidation()
    idValidationError = idValidation.validate(getReview)

    match request.method:
        case "GET":
            if idValidationError:
                return idValidationError, 422

            else:
                review = db.query(Review).where(Review.id == getReview["id"]).first()

                if not review:
                    return "Review not found", 404
                
                else:
                    result = {
                        "id": review.id,
                        "user": review.user.username,
                        "book": f"{review.book.title} by {review.book.author}",
                        "content": review.content
                    }

                    return jsonify(result), 200

        case "POST":
            createReviewValidationError = createReviewValidation.validate(getReview)

            if createReviewValidationError:
                return createReviewValidationError, 422
            
            else:
                getUser = db.query(User).where(User.id == int(getReview["userId"])).first()
                getBook = db.query(Book).where(Book.id == int(getReview["bookId"])).first()

                if not getBook or not getUser:
                    return "Book or user not found", 404
                
                else:
                    newReview = Review(
                        user=getUser,
                        book=getBook,
                        content=getReview["content"]
                    )

                    db.add(newReview)
                    db.commit()
                    return "Review made", 200
            
        
        case "DELETE":
            if idValidationError:
                return idValidationError, 422

            else:
                deletedReview = db.query(Review).where(Review.id == getReview["id"]).first()

                if not deletedReview:
                    return "Review not found", 200
                
                else:
                    db.delete(deletedReview)
                    db.commit()
                    return f"Review id:{deletedReview.id}, has be deleted", 200

# TODO: intergrate (https://openlibrary.org/developers/api)
@app.route("/admin")
def admin_add_book():
    ...

if __name__ == "__main__":
    app.run(port=5000, debug=True)