from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine, desc
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Author(Base):
	__tablename__ = 'author'
	id = Column(Integer, primary_key=True)
	name = Column(String)

	def __init__(self, name):
		self.name = name

class Book(Base):
	__tablename__ = 'book'
	id = Column(Integer, primary_key=True)
	title = Column(String)

	def __init__(self, title):
		self.title = title

class BookAndAuthor(Base):
	__tablename__ = 'book_and_author'
	id = Column(Integer, primary_key=True)
	book_id = Column(Integer, ForeignKey('book.id'))
	author_id = Column(Integer, ForeignKey('author.id'))

	def __init__(self, author_id, book_id):
		self.author_id = author_id
		self.book_id = book_id