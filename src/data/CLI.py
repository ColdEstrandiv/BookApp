from data import User, Library, Book, Review, BookProgress, ReadingSession
import click
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from sqlalchemy.exc import IntegrityError

engine = create_engine("sqlite:///data/data.sqlite", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

#TODO: Exception handling for duplicate unique entries, or bad inputs

@click.group()
def cli():
    pass

@click.command(help="-d firstName < >, -d lastName < >, username < >, -d email < >, -d password < >")
@click.option("--dict", "-d", "cliDict", type=(str, str), multiple=True,)
def create_user(cliDict):
    newUserDict = dict(cliDict)
    # click.echo(newUserDict["firstName"])
    newUser = User(firstName=newUserDict["firstName"], 
    lastName=newUserDict["lastName"],
    username=newUserDict["username"],
    email=newUserDict["email"], 
    password=newUserDict["password"])
    
    session.add(newUser)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        print("username or email already in use")

@click.command(help="<username> <libraryName>")
@click.argument("user")
@click.argument("library_name")
def create_library(user, library_name):
    userDb = session.query(User).where(User.username == str(user)).first()
    newLibrary = Library(name=library_name, user=userDb)

    session.add(newLibrary)
    session.commit()

@click.command(help="-d title < >, -d author < >, -d pageCount < >")
@click.option("--dict", "-d", "cliDict", type=(str, str), multiple=True,)
def create_book(cliDict):
    newBookDict = dict(cliDict)
    newBook = Book(title=newBookDict["title"], 
    author=newBookDict["author"],
    pageCount=int(newBookDict["pageCount"]))

    session.add(newBook)
    session.commit()

@click.command(help="<bookId> <username> <body>")
@click.argument("book_id")
@click.argument("username")
@click.argument("body")
def create_review(book_id, username, body):
    userDb = session.query(User).where(User.username == str(username)).first()
    bookDb = session.query(Book).where(Book.id == int(book_id)).first()
    newReview = Review(user=userDb, book=bookDb, content=str(body))

    session.add(newReview)
    session.commit()

@click.command(help="<username> <bookId>")
@click.argument("username")
@click.argument("book_id")
def create_book_progress(username, book_id):
    userDb = session.query(User).where(User.username == str(username)).first()
    bookDb = session.query(Book).where(Book.id == int(book_id)).first()
    newBookProg = BookProgress(user=userDb, book=bookDb)

    session.add(newBookProg)
    session.commit()
    
@click.command(help="<bookProgressId> <page_count> <time in HH:MM>")
@click.argument("bookprog_id")
@click.argument("page_count")
@click.argument("readtime")
def create_read_session(bookprog_id, page_count, readtime):
    bookProgDb = session.query(BookProgress).where(BookProgress.id == int(bookprog_id)).first()
    timeObject = datetime.strptime(readtime, "%H:%M").time()
    newReadSession = ReadingSession(bookProgress=bookProgDb, pageCount = int(page_count), readTime = timeObject)

    session.add(newReadSession)
    session.commit()

@click.command(help="<libraryId> <bookId>")
@click.argument("library_id")
@click.argument("book_id")
def add_library_book(library_id, book_id):
    libraryDb = session.query(Library).where(Library.id == int(library_id)).first()
    bookDb = session.query(Book).where(Book.id == int(book_id)).first()

    libraryDb.books.append(bookDb)
    session.commit()

@click.command(help="<bookProgressId>")
@click.argument("book_progress_id")
def complete_book(book_progress_id):
    bookProgressDb = session.query(BookProgress).where(BookProgress.id == int(book_progress_id)).first()

    bookProgressDb.status = "Completed"
    session.commit()

# @click.command(help="<username> <password>")
# @click.argument("admin_username")
# @click.argument("admin_password")
# def create_admin(admin_username, admin_password):
#     new_admin = Admin(username=admin_username, password=admin_password)
    
#     session.add(new_admin)
#     session.commit()

@click.command(help="<Object> <id>")
@click.argument("object")
@click.argument("object_id")
def del_obj_id(object, object_id):
    match str(object):
        case "readingSession":
            deletedEntity = session.query(ReadingSession).where(ReadingSession.id == int(object_id)).first()
            session.delete(deletedEntity)
            session.commit()


cli.add_command(create_user)
cli.add_command(create_library)
cli.add_command(create_book)
cli.add_command(create_review)
cli.add_command(create_book_progress)
cli.add_command(create_read_session)
cli.add_command(add_library_book)
cli.add_command(complete_book)
cli.add_command(del_obj_id)
# cli.add_command(create_admin)

if __name__ == "__main__":
    cli()