from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import User, Library, Book, LibraryBook, Review, BookProgress, ReadingSession
import click
from pprint import pprint

engine = create_engine("sqlite:///data.sqlite", echo=False)
Session = sessionmaker(bind=engine)
db = Session()

@click.group()
def cli():
    pass

# TODO: suggest doing this by id or adding username to USER as an unique key
@click.command
@click.argument('username')
def get_user(username):
    user = db.query(User).filter(User.userName==str(username)).first()
    
    libraries = db.query(Library).filter(Library.owner == user.id).all()
    librariesId = []
    
    for i in range(len(libraries)):
        librariesId.append(libraries[i].id)
    
    bookprogress = db.query(BookProgress).filter(BookProgress.user == user.id).all()
    allReading = []

    for i in range(len(bookprogress)):
        reading = db.query(ReadingSession).filter(ReadingSession.bookProgressId == bookprogress[i].id).all()
        readingData = (f'ID: {reading[i].id}, BookProgressID: {reading[i].bookProgressId}, Start: {reading[i].start}, Stop: {reading[i].stop}')
        allReading.append(readingData)


    print(f'User \n ID: {user.id}, Name {user.firstName} {user.lastName}, Email {user.email}, Password {user.password}')
    print(f'Library ids: {librariesId}')
    pprint(allReading)

@click.command
@click.argument('booktitle')
def get_book(booktitle):
    getBook = db.query(Book).filter(Book.title==str(booktitle)).first()
    
    libraryBook = db.query(LibraryBook).filter(LibraryBook.bookId==getBook.id).all()
    librayIds = []
    userIds = []

    for i in range(len(libraryBook)):
        librayIds.append(libraryBook[i].libraryId)
    
    for i in range(len(librayIds)):
        findUser = db.query(Library)



cli.add_command(get_book)
cli.add_command(get_user)

if __name__ == "__main__":
    cli()