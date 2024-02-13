from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Session
from models import User, Library, Book, LibraryBook, Review, BookProgress, ReadingSession
import click
from CLI import create_book, create_book_progress, create_library, create_library_book
from CLI import create_user, create_review, create_read_session
engine = create_engine('sqlite:///data.sqlite')

# export functions here

#TODO: initialize tables    
#querey functions

# def getUserLibraries(userId):
#     ...

# @click.command()
# @ click
# def createUser(userInfo: dict):
#     newUser = {
#         'firstName': userInfo['firstName'],
#         'lastName': userInfo['lastName'],
#         'email': userInfo['email']
#     }
#     createUser = User.create(newUser)

# if __name__ == "__main__":


#     user = createUser