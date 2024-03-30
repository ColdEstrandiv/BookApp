from flask import Flask
from flask_cors import CORS
from blueprints import userById, createNewUser, bookProgressById, createBookProgress, getUserLibraries, library, creatNewLibrary, userReadsById, createNewBook, getBookbyId, createNewRead, getReadById
from blueprints import createNewReview, getReviewById, addLibraryBook, getBookReaders, getAllusers, getAllBooks, getUserReviews

app = Flask(__name__)
CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

# /user
app.register_blueprint(getAllusers)

# /user/<id>
app.register_blueprint(userById)

# /user
app.register_blueprint(createNewUser)

# /user/<id>/libraries
app.register_blueprint(getUserLibraries)

# /user/<id>/reads
app.register_blueprint(userReadsById)

# /bookProgress/<id>
app.register_blueprint(bookProgressById)

# /user/<uId>bookProgress/book/<bId>
app.register_blueprint(createBookProgress)

# /bookProgress/<id>/read
app.register_blueprint(createNewRead)

# /read/<id>
app.register_blueprint(getReadById)

# /library/<id>
app.register_blueprint(library)

# /library/<lId>/book/<bId>
app.register_blueprint(addLibraryBook)

# /user/<id>/library
app.register_blueprint(creatNewLibrary)

# /books
app.register_blueprint(getAllBooks)

# /book
app.register_blueprint(createNewBook)

# /book/<id>
app.register_blueprint(getBookbyId)

# /book/<id>/readers
app.register_blueprint(getBookReaders)

# /user/<uId>/book/<bId>
app.register_blueprint(createNewReview)

# /user/<uId>/reviews
app.register_blueprint(getUserReviews)

# /review/<id>
app.register_blueprint(getReviewById)

if __name__ == '__main__':
    app.run(port=5000, debug=True)