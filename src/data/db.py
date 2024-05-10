from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import g
from .models import Base

engine = create_engine("sqlite:///data/data.sqlite", echo=True)
Session = sessionmaker(bind=engine)
session = Session()
def get_db():
    if 'db' not in g:
        g.db = session

    return g.db

def close_db(_):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    Base.metadata.create_all(engine, checkfirst=True)

    app.teardown_appcontext(close_db)