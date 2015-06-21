from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from datetime import datetime

engine = create_engine('sqlite:///dbMyBlog.db', echo=True)
Base = declarative_base()

class User(Base):
    """"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __init__(self, username, password):
        """"""
        self.username = username
        self.password = password



class Post(Base):
    """"""
    __tablename__ = "Blog"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=True)
    body = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())

    def __init__(self, title, body):
        """"""
        self.title = title
        self.body = body


# create tables
Base.metadata.create_all(engine)
