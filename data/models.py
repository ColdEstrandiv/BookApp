# export functions here

from sqlalchemy import String
from sqlalchemy.orm import declarative_base, DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Integer
import click

engine = create_engine("sqlite:///data/main.sqlite", echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class Base(DeclarativeBase):
    ...

class User(Base):
    __tablename__ = "user"
    id = mapped_column(Integer, primary_key=True)
    firstName = mapped_column(String())
    lastName = mapped_column(String())
    email = mapped_column(String())
    password = mapped_column(String())

class library(Base):
    __tablename__ = "library"
    id = mapped_column(Integer, primary_key=True)
    owner = mapped_column(ForeignKey("user.id"))

class libraryBook(Base):
    __tablename__ = "libraryBook"
    id = mapped_column(Integer, primary_key=True)
    bookId = mapped_column(ForeignKey("book.id")) 
    libraryId = mapped_column(ForeignKey("library.id"))

class Book(Base):
    __tablename__ = "book"
    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String())
    author = mapped_column(String())

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

class ReadingSession(Base):
    __tablename__ = "readingSession"
    id = mapped_column(Integer, primary_key=True)
    bookProgressId = mapped_column(ForeignKey("bookProgress.id"))
    start = mapped_column(String())
    stop = mapped_column(String())

# This checks if tables exists and creates them if they dont
Base.metadata.create_all(engine, checkfirst=True)
