from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime, Time
from sqlalchemy import Table
from datetime import datetime

engine = create_engine("sqlite:///data.sqlite", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class Base(DeclarativeBase):
    ...

class User(Base):
    __tablename__ = "user"
    id = mapped_column(Integer, primary_key=True)
    firstName = mapped_column(String())
    lastName = mapped_column(String())
    userName = mapped_column(String(), unique=True)
    email = mapped_column(String(), unique=True)
    password = mapped_column(String())

    libraries = relationship("Library", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    bookProgresses = relationship("BookProgress", back_populates="user")
    
library_book_association = Table('library_book_association', Base.metadata,
Column('library_id', Integer, ForeignKey('library.id')),
Column('book_id', Integer, ForeignKey('book.id')))

class Library(Base):
    __tablename__ = "library"
    name = mapped_column(String())
    id = mapped_column(Integer, primary_key=True)
    userId = mapped_column(ForeignKey("user.id"))

    # The secondary and "library_book_association" is required for many-to-many relationships
    books = relationship("Book", secondary="library_book_association", back_populates= "libraries")
    user = relationship("User", back_populates= "libraries")




class Book(Base):
    __tablename__ = "book"
    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String())
    author = mapped_column(String())
    pageCount = mapped_column(Integer())

    libraries = relationship("Library", secondary="library_book_association", back_populates="books")
    reviews = relationship("Review", back_populates="book")
    bookProgresses = relationship("BookProgress", back_populates="book")

class Review(Base):
    __tablename__ = "review"
    id = mapped_column(Integer, primary_key=True)
    userId = mapped_column(ForeignKey("user.id"))
    bookId = mapped_column(ForeignKey("book.id"))
    content = mapped_column(String())

    user = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")

class BookProgress(Base):
    __tablename__ = "bookProgress"
    id = mapped_column(Integer, primary_key=True)
    userId = mapped_column(ForeignKey("user.id"))
    bookId = mapped_column(ForeignKey("book.id"))
    # status = Started, Finished
    status = mapped_column(String(), default= "Started")

    user = relationship("User", back_populates="bookProgresses")
    readingSessions = relationship("ReadingSession", back_populates="bookProgress")
    book = relationship("Book", back_populates="bookProgresses")

class ReadingSession(Base):
    __tablename__ = "readingSession"
    id = mapped_column(Integer, primary_key=True)
    bookProgressId = mapped_column(ForeignKey("bookProgress.id"))
    pageCount = mapped_column(Integer())
    date = mapped_column(DateTime, default=datetime.utcnow)
    time = mapped_column(Time())

    bookProgress = relationship("BookProgress", back_populates= "readingSessions")

# This checks if tables exists and creates them if they dont
Base.metadata.create_all(engine, checkfirst=True)