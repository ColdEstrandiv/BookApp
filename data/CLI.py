from models import User, Library, Book, LibraryBook, Review, BookProgress, ReadingSession
import click
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine("sqlite:///data.sqlite", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

#TODO: could maybe make all off these one function taking an argument then a dictionary

@click.group()
def cli():
    pass

@click.command(help="-d firstName < >, -d lastName < >, userName < >, -d email < >, -d password < >")
@click.option("--dict", "-d", "cliDict", type=(str, str), multiple=True,)
def create_user(cliDict):
    newUserDict = dict(cliDict)
    # click.echo(newUserDict["firstName"])
    newUser = User(firstName=newUserDict['firstName'], 
    lastName=newUserDict['lastName'],
    userName=newUserDict['userName'],
    email=newUserDict['email'], 
    password=newUserDict['password'])
    
    session.add(newUser)
    session.commit()

@click.command(help="<userId>")
@click.argument("userId")
def create_library(userid):
    newLibrary = Library(owner=int(userid))

    session.add(newLibrary)
    session.commit()

@click.command(help="-d title < >, -d author < >, -d pageCount < >")
@click.option("--dict", "-d", "cliDict", type=(str, str), multiple=True,)
def create_book(cliDict):
    newBookDict = dict(cliDict)
    newBook = Book(title=newBookDict['title'], 
    author=newBookDict['author'])

    session.add(newBook)
    session.commit()

@click.command(help="<bookId> <libraryId>")
@click.argument('book')
@click.argument('library')
def create_library_book(book, library):
    newLibraryBook = LibraryBook(bookId=int(book), libraryId=int(library))

    session.add(newLibraryBook)
    session.commit()

@click.command(help="<bookId> <userId> <body>")
@click.argument('bookid')
@click.argument('userid')
@click.argument('body')
def create_review(bookid, userid, body):
    newReview = Review(user=userid, book=bookid, content=str(body))

    session.add(newReview)
    session.commit()

@click.command(help="<userId> <bookId> <status>")
@click.argument('userid')
@click.argument('bookid')
@click.argument('state')
def create_book_progress(userid, bookid, state):
    newBookProg = BookProgress(user=userid, book=bookid, status=state)

    session.add(newBookProg)
    session.commit()
    
@click.command(help="<bookProgressId> <start> <stop>")
@click.argument('bookprogid')
@click.argument('startpg')
@click.argument('stoppg')
@click.argument('datedata')
@click.argument('readtime')
def create_read_session(bookprogid, startpg, stoppg, datedata, readtime):
    newReadSession = ReadingSession(bookProgressId=bookprogid, start=startpg, stop=stoppg, date=datedata, time=readtime)

    session.add(newReadSession)
    session.commit()


cli.add_command(create_user)
cli.add_command(create_library)
cli.add_command(create_book)
cli.add_command(create_library_book)
cli.add_command(create_review)
cli.add_command(create_book_progress)
cli.add_command(create_read_session)



if __name__ == '__main__':
    cli()