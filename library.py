#!/venv/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import re
import os
from flask import Flask, request, session, g, redirect, jsonify, url_for, abort, \
     render_template, flash	
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine, desc, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Author, Book
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

@app.route('/search', methods=['POST', 'GET'])
def search():
	if request.method == 'POST':
		keyword = request.form['keyword']
		books = session_sql.query(Book).filter(Book.title.like('%' + keyword + '%')).all()
		authors = session_sql.query(Author).filter(Author.name.like('%' + keyword + '%')).all()

		if books or authors:
			return render_template('search.html', books=books, authors=authors)

		flash('There are no results.')
	return render_template('search.html')

@app.route('/authors')
def authors():
    authors = session_sql.query(Author).order_by(desc(Author.id)).all()
    return render_template('authors.html', authors=authors)

@app.route('/edit_author/<int:id>', methods=['POST', 'GET'])
def edit_author(id):
	if not session.get('logged_in'):
		abort(401)

	form = AuthorForm(request.form)
	author = session_sql.query(Author).get(id)

	if request.method == 'POST' and form.validate():
		author.name = form.name.data

		for book_id in form.books.choices:
			book = session_sql.query(Book).get(book_id)
			author.book.append(book)

		flash('Author was successfully update')
		return redirect(url_for('authors'))

	form.name.data = author.name
	books = session_sql.query(Book).order_by(desc(Book.id)).all()
	form.books.choices = [(book.id, book.title) for book in books]

	books = author.book
	form.books.default = [book.id for book in books]
	session_sql.commit()
	return render_template('edit_author.html', form=form, author=author)

@app.route('/delete_author/<int:id>', methods=['GET'])
def delete_author(id):
	if not session.get('logged_in'):
		abort(401)

	author = session_sql.query(Author).get(id)
	session_sql.delete(author)
	session_sql.commit()
	flash('Author was successfully delete')
	return redirect(url_for('authors'))

@app.route('/delete_author_list', methods=['POST'])
def delete_author_list():
	if not session.get('logged_in'):
		return jsonify(error='please log in')

	ids = [int(arg) for arg in request.form['ids'].split(',')]
	session_sql.query(Author).filter(Author.id.in_(ids)).delete(synchronize_session='fetch')
	session_sql.commit()
	return jsonify(redirect='authors')

@app.route('/add_author', methods=['POST', 'GET'])
def add_author():
	if not session.get('logged_in'):
		abort(401)

	form = AuthorForm(request.form)

	if request.method == 'POST' and form.validate():
		author = Author(form.name.data)
		session_sql.add(author)
		session_sql.commit()

		for book_id in form.books.choices:
			book = session_sql.query(Book).get(book_id)
			author.book.append(book)

		session_sql.commit()
		flash('New author was successfully add')
		return redirect(url_for('authors'))

	books = session_sql.query(Book).order_by(desc(Book.id)).all()
	form.books.choices = [(book.id, book.title) for book in books]
	return render_template('add_author.html', form=form)



@app.route('/books')
def books():
    books = session_sql.query(Book).order_by(desc(Book.id)).all()
    return render_template('books.html', books=books)

@app.route('/add_book', methods=['POST', 'GET'])
def add_book():
	if not session.get('logged_in'):
		abort(401)

	form = BookForm(request.form)

	if request.method == 'POST' and form.validate():
		book = Book(form.title.data)
		session_sql.add(book)
		session_sql.commit()

		for author_id in form.authors.choices:
			author = session_sql.query(Author).get(author_id)
			book.authors.append(author)

		session_sql.commit()
		flash('New book was successfully add')
		return redirect(url_for('books'))

	authors = session_sql.query(Author).order_by(desc(Author.id)).all()
	form.authors.choices = [(author.id, author.name) for author in authors]
	session_sql.commit()
	return render_template('add_book.html', form=form)

@app.route('/edit_book/<int:id>', methods=['POST', 'GET'])
def edit_book(id):
	if not session.get('logged_in'):
		abort(401)

	form = BookForm(request.form)
	book = session_sql.query(Book).get(id)

	if request.method == 'POST' and form.validate():
		book.title = form.title.data

		for author_id in form.authors.choices:
			author = session_sql.query(Book).get(book_id)
			book.authors.append(author)

		session_sql.commit()
		flash('Book was successfully update')
		return redirect(url_for('books'))

	form.title.data = book.title
	authors = session_sql.query(Author).order_by(desc(Author.id)).all()
	form.authors.choices = [(author.id, author.name) for author in authors]

	authors = book.authors
	form.authors.default = [author.id for author in authors]
	return render_template('edit_book.html', book=book, form=form)

@app.route('/delete_book/<int:id>')
def delete_book(id):
	if not session.get('logged_in'):
		abort(401)

	book = session_sql.query(Book).get(id)
	session_sql.delete(book)
	session_sql.commit()
	flash('Book was successfully delete')
	return redirect(url_for('books'))

@app.route('/delete_book_list', methods=['POST'])
def delete_book_list():
	if not session.get('logged_in'):
		return jsonify(error='please log in')

	ids = [int(arg) for arg in request.form['ids'].split(',')]
	session_sql.query(Book).filter(Book.id.in_(ids)).delete(synchronize_session='fetch')
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