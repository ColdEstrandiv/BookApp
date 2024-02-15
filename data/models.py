from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Integer


engine = create_engine("sqlite:///data.sqlite", echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class Base(DeclarativeBase):
    ...

# TODO: add username unique column
class User(Base):
    __tablename__ = "user"
    id = mapped_column(Integer, primary_key=True)
    firstName = mapped_column(String())
    lastName = mapped_column(String())
    userName = mapped_column(String())
    email = mapped_column(String())
    password = mapped_column(String())

# TODO: maybe add name column
class Library(Base):
    __tablename__ = "library"
    name = mapped_column(String())
    id = mapped_column(Integer, primary_key=True)
    owner = mapped_column(ForeignKey("user.id"))

# TODO: Devise a way to determine if the user who owns the library has finished the book
    # maybe add page count too "Book" and write a function to add up Readingsessions in Bookprogress
class LibraryBook(Base):
    __tablename__ = "libraryBook"
    id = mapped_column(Integer, primary_key=True)
    bookId = mapped_column(ForeignKey("book.id")) 
    libraryId = mapped_column(ForeignKey("library.id"))

class Book(Base):
    __tablename__ = "book"
    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String())
    author = mapped_column(String())
    pageCount = mapped_column(Integer())

class Review(Base):
    __tablename__ = "review"
    id = mapped_column(Integer, primary_key=True)
    user = mapped_column(ForeignKey("user.id"))
    book = mapped_column(ForeignKey("book.id"))
    content = mapped_column(String())

class BookProgress(Base):
    __tablename__ = "bookProgress"
    id = mapped_column(Integer, primary_key=True)
    user = mapped_column(ForeignKey("user.id"))
    book = mapped_column(ForeignKey("book.id"))
    # status = To Be Read, Started, Finished
    status = mapped_column(String())

class ReadingSession(Base):
    __tablename__ = "readingSession"
    id = mapped_column(Integer, primary_key=True)
    bookProgressId = mapped_column(ForeignKey("bookProgress.id"))
    start = mapped_column(String())
    stop = mapped_column(String())
    date = mapped_column(String())
    time = mapped_column(String())



# This checks if tables exists and creates them if they dont
Base.metadata.create_all(engine, checkfirst=True)
