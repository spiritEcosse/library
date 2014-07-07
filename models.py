from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

book_and_author = Table('book_and_author', Base.metadata,
    Column('book_id', Integer, ForeignKey('book.id')),
    Column('author_id', Integer, ForeignKey('author.id'))
)

class Author(Base):
	__tablename__ = 'author'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	book = relationship("Book",
                    secondary = lambda: book_and_author,
                    backref="authors")

	def __init__(self, name):
		self.name = name

class Book(Base):
	__tablename__ = 'book'
	id = Column(Integer, primary_key=True)
	title = Column(String)

	def __init__(self, title):
		self.title = title
