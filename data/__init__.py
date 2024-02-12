from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Session
from .models import User, library, Book, libraryBook, Review, BookProgress, ReadingSession
import click
engine = create_engine('sqlite:///data.db')

# export functions here

#TODO: initialize tables    
#querey functions

def getUserLibraries(userId):
    ...

@click.command()
@ click
def createUser(userInfo: dict):
    newUser = {
        'firstName': userInfo['firstName'],
        'lastName': userInfo['lastName'],
        'email': userInfo['email']
    }
    createUser = User.create(newUser)

if __name__ == "__main__":


    user = createUser