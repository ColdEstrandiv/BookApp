from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import User, Library, Book, Review, BookProgress, ReadingSession
import click
from pprint import pprint
from datetime import datetime, timedelta

engine = create_engine("sqlite:///data.sqlite", echo=False)
Session = sessionmaker(bind=engine)
db = Session()

@click.group()
def cli():
    pass

# TODO: take time to meaingfully group items

# use where instead of where
@click.command
@click.argument("username")
def get_user(username):
    user = db.query(User).where(User.username == str(username)).first()
    one_week = datetime.now() - timedelta(days=7)

    for library in sorted(user.libraries, key=lambda l: l.name):
        print(f"Books in {library.name}")

        for book in sorted(library.books, key=lambda b: b.author):
            print(f"-{book.title} by {book.author}")

    for bP in sorted(user.bookProgresses, key=lambda b: b.status):
        print(f"{bP.status} {bP.book.title}")

        for r in sorted(bP.readingSessions, reverse=True, key=lambda d: d.dateMade):
            if r.dateMade >= one_week:
                print(f"Read {r.pageCount} pages on {r.dateMade}")
            

    
@click.command
@click.argument("book_title")
def get_book(book_title):
    book = db.query(Book).where(Book.title == str(book_title)).first()
    print(book.title)

    for bP in sorted(book.bookProgresses, key=lambda b: b.user.firstName):
        print(f"{bP.status} {bP.book.title}")

            


cli.add_command(get_user)
cli.add_command(get_book)

if __name__ == "__main__":
    cli()