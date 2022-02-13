import flask
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

URI = 'sqlite:///new-books-collection.db'

##CREATE FLASK APP
app = Flask(__name__)

##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CREATE TABLE
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book> {self.title}'

if not os.path.isfile(URI):
    db.create_all()

all_books = db.session.query(Book).all()

@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template('index.html', books=all_books)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == 'POST':
        book_title = request.form.get("title")
        print(book_title)
        book_author = request.form.get("author")
        book_rating = request.form.get("rating")

        new_book = Book(title=book_title, author=book_author, rating=book_rating)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add.html')

##CREATE EDIT PAGE
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if request.method == 'POST':
        
        new_rating = request.form.get("rating")

        book_to_update = Book.query.get(id)
        book_to_update.rating = new_rating
        db.session.commit()

        return redirect(url_for('home'))
    else:
        all_books = db.session.query(Book).all()
        return render_template('edit.html', book=all_books[id-1])

##CREATE DELETE FUNCTION
@app.route("/delete/<int:id>")
def delete_book(id):
    
    book_to_delete = Book.query.get(id)
    db.session.delete(book_to_delete)
    db.session.commit()
    
    all_books = db.session.query(Book).all()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True) 

