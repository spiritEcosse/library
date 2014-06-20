#!/venv/bin/python
# -*- coding: utf8 -*-

import sqlite3
import os
from flask import Flask, request, session, g, redirect, jsonify, url_for, abort, \
     render_template, flash	
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine, desc, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Author, Book, BookAndAuthor
from forms import BookForm, AuthorForm

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'library.db'),
    DEBUG=True,
    SECRET_KEY='spirit!@#ECOSE123',
    USERNAME='admin',
    PASSWORD='1111'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

engine = create_engine('sqlite:///' + os.path.join(app.root_path, 'library.db'))
Session = sessionmaker(bind=engine)
session_sql = Session()

def init_db():
	with app.app_context():
		with app.open_resource('schema.sql', mode='r') as f:
			session_sql.execute(f.read())
		session_sql.commit()

@app.route('/')
def index():
    entities = {'Books': 'books', 'Authors': 'authors'}
    return render_template('index.html', entities=entities)


@app.route('/authors')
def authors():
    authors = session_sql.query(Author).order_by(desc(Author.id)).all()
    return render_template('authors.html', authors=authors)

@app.route('/edit_author/<int:id>', methods=['POST', 'GET'])
def edit_author(id):
	if not session.get('logged_in'):
		abort(401)

	form = AuthorForm(request.form)

	if request.method == 'POST':
		session_sql.query(Author).filter(Author.id==id).update({Author.name: form.name.data})
		session_sql.query(BookAndAuthor).filter(BookAndAuthor.author_id==id).delete()

		# добавить пачку
		for book_id in form.books.choices:
			session_sql.add(BookAndAuthor(id, book_id))

		session_sql.commit()
		flash('Author was successfully update')
		return redirect(url_for('authors'))

	author = session_sql.query(Author).filter(Author.id==id).one()
	books = session_sql.query(Book).order_by(desc(Book.id)).all()
	form.name.data = author.name
	form.books.choices = [(book.id, book.title) for book in books]

	# author = session_sql.query(Author).filter(Author.id==id).one()
	# join Author BookAndAuthor
	# books = session_sql.query(Book).order_by(desc(Book.id)).all()
	book_and_author = session_sql.query(BookAndAuthor).filter(BookAndAuthor.author_id==id).all()
	form.books.default = [book.book_id for book in book_and_author]
	# books_author = []

	# for data in book_and_author:
		# books_author.append(data.book_id)
	return render_template('edit_author.html', form=form, author=author)

@app.route('/delete_author/<int:id>', methods=['GET'])
def delete_author(id):
	if not session.get('logged_in'):
		abort(401)

	session_sql.query(Author).filter(Author.id==id).delete()
	# join
	session_sql.query(BookAndAuthor).filter(BookAndAuthor.author_id==id).delete()
	session_sql.commit()
	flash('Author was successfully delete')
	return redirect(url_for('authors'))

@app.route('/delete_author_list', methods=['POST'])
def delete_author_list():
	if not session.get('logged_in'):
		return jsonify(error='please log in')

	ids = [int(arg) for arg in request.form['ids'].split(',')]
	session_sql.query(Author).filter(Author.id.in_(ids)).delete(synchronize_session='fetch')
	# join
	session_sql.query(BookAndAuthor).filter(BookAndAuthor.author_id.in_(ids)).delete(synchronize_session='fetch')
	session_sql.commit()
	return jsonify(redirect='authors')

@app.route('/add_author', methods=['POST', 'GET'])
def add_author():
	if not session.get('logged_in'):
		abort(401)

	if request.method == 'POST':
		author = Author(request.form['name'])
		session_sql.add(author)
		session_sql.commit()

		# добавить пачку
		for book_id in request.form.getlist('books'):
			session_sql.add(BookAndAuthor(author.id, book_id))

		session_sql.commit()
		flash('New author was successfully posted')
		return redirect(url_for('authors'))

	books = session_sql.query(Book).order_by(desc(Book.id)).all()
	return render_template('add_author.html', books=books)



@app.route('/books')
def books():
    books = session_sql.query(Book).order_by(desc(Book.id)).all()
    return render_template('books.html', books=books)

@app.route('/add_book', methods=['POST', 'GET'])
def add_book():
	if not session.get('logged_in'):
		abort(401)

	if request.method == 'POST':
		book = Book(request.form['title'])
		session_sql.add(book)
		session_sql.commit()

		# добавить пачку
		for author_id in request.form.getlist('authors'):
			session_sql.add(BookAndAuthor(author_id, book.id))

		session_sql.commit()
		flash('New book was successfully posted')
		return redirect(url_for('books'))

	authors = session_sql.query(Author).order_by(desc(Author.id)).all()
	return render_template('add_book.html', authors=authors)

@app.route('/edit_book/<int:id>', methods=['POST', 'GET'])
def edit_book(id):
	if not session.get('logged_in'):
		abort(401)

	if request.method == 'POST':
		session_sql.query(Book).filter(Book.id==id).update({Book.title: request.form['title']})
		session_sql.query(BookAndAuthor).filter(BookAndAuthor.book_id==id).delete()

		# добавить пачку
		for author_id in request.form.getlist('authors'):
			session_sql.add(BookAndAuthor(author_id, id))

		session_sql.commit()
		flash('Book was successfully update')
		return redirect(url_for('books'))

	book = session_sql.query(Book).filter(Book.id==id).one()
	# join Author BookAndAuthor
	authors = session_sql.query(Author).order_by(desc(Author.id)).all()
	book_and_author = session_sql.query(BookAndAuthor).filter(BookAndAuthor.book_id==id).all()
	authors_book = []

	for data in book_and_author:
		authors_book.append(data.author_id)

	session_sql.commit()
	return render_template('edit_book.html', book=book, authors=authors, authors_book=authors_book)

@app.route('/delete_book/<int:id>')
def delete_book(id):
	if not session.get('logged_in'):
		abort(401)

	session_sql.query(Book).filter(Book.id==id).delete()
	# join
	session_sql.query(BookAndAuthor).filter(BookAndAuthor.book_id==id).delete()
	session_sql.commit()
	flash('Book was successfully delete')
	return redirect(url_for('books'))

@app.route('/delete_book_list', methods=['POST'])
def delete_book_list():
	if not session.get('logged_in'):
		return jsonify(error='please log in')

	ids = [int(arg) for arg in request.form['ids'].split(',')]
	session_sql.query(Book).filter(Book.id.in_(ids)).delete(synchronize_session='fetch')
	# join
	session_sql.query(BookAndAuthor).filter(BookAndAuthor.book_id.in_(ids)).delete(synchronize_session='fetch')
	session_sql.commit()
	return jsonify(redirect='books')




@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

if __name__ == "__main__":
	app.run()