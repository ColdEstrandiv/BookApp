# export functions here

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id = mapped_column(primary_key=True)
    firstName = mapped_column(String())
    lastName = mapped_column(String())
    email = mapped_column(String())

    

class library(Base):
    __table__ = "library"
    id = mapped_column(primary_key=True)
    owner = mapped_column(ForeignKey("user.id"))

class library(Base):
    __table__ = "library"
    id = mapped_column(primary_key=True)
    bookId = mapped_column(ForeignKey("book.id")) 
    libraryId = mapped_column(ForeignKey("library.id"))

class Book(Base):
    __table__ = "library"
    id = mapped_column(primary_key=True)
    title = mapped_column(String())
    author = mapped_column(String())

class Review(Base):
    __tablename__ = "review"
    id = mapped_column(primary_key=True)
    user = mapped_column(ForeignKey("user.id"))
    book = mapped_column(ForeignKey("book.id"))
    content = mapped_column(String())

class BookProgress(Base):
    __tablename__ = "bookProgress"
    id = mapped_column(primary_key=True)
    user = mapped_column(ForeignKey("user.id"))
    book = mapped_column(ForeignKey("book.id"))

class ReadingSession(Base):
    __tablename__ = "readingSession"
    id = mapped_column(primary_key=True)
    bookProgressId = mapped_column(ForeignKey("bookProgress.id"))
    start = mapped_column(String())
    stop = mapped_column(String())

