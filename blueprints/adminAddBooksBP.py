from flask import Blueprint

adminAddBookBp = Blueprint('book', __name__)

@adminAddBookBp.route('/adminAddBook')
def adminAddBook ():
    ...