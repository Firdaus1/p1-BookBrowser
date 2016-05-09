import flask
import json
from flask import Flask

authors = dict()
books = dict()
editionCount = 0
bio = list()

with open('data/books.json', 'r', encoding='utf-8') as jf:
    booklist = json.load(jf)
    for book in booklist:
        books[book['id']] = book
        for edition in book['editions']:
            editionCount += 1

with open('data/authors.json', 'r', encoding='utf-8') as jf:
    authorlist = json.load(jf)
    for author in authorlist:
        if author['name'] is None:
            author['name'] = 'Anonymous'
        authors[author['id']] = author
        if 'bio' in author and isinstance(author['bio'], str):
            author['bio'] = author['bio'].splitlines()

app = Flask(__name__)

@app.route('/')
def index():
    return flask.render_template("index.html", bookCount=len(books), authorCount=len(authors),
                                 editionCount=editionCount, booklist=booklist, authorlist=authorlist)

@app.route('/authors/')
def authorslist():
    title = "Author list"
    return flask.render_template('authorlist.html', title=title, authors=authors.values())

@app.route('/books/')
def bookslist():
    title = "Book List"
    return flask.render_template('booklist.html', title=title, books=books.values())

@app.route('/author/<aid>')
def authorpage(aid):
    title = "Author"
    if authors[aid]:
        tempbooklist = []
        for book in books.values():
            for a in book['authors']:
                if a == aid:
                    tempbooklist.append(book)
        return flask.render_template('author.html', title=title, author=authors[aid], books=tempbooklist)
    else:
        return flask.abort(404)

@app.route('/book/<bid>')
def bookpage(bid):
    title = "Book"
    if books[bid]:
        tempauthorlist = []

        cover = ''
        for author_id in books[bid]['authors']:
            tempauthorlist.append(authors[author_id])
        for edition in books[bid]['editions']:
            if 'cover' in edition.keys():
                cover = edition['cover']
                break
        return flask.render_template('book.html', title=title, book=books[bid], authors=tempauthorlist,
                                     cover=cover)
    else:
        return flask.abort(404)

@app.route('/books/<bid>/editions/<eid>')
def editionpage(bid, eid):
    title ="Editions"
    cover = ''
    for edition in books[bid]['editions']:
        if edition['id'] == eid:
            if 'cover' in edition.keys():
                cover = edition['cover']
            tempauthors = []
            for au in edition['authors']:
                tempauthors.append(authors[au])
            return flask.render_template('edition.html', title=title, cover=cover, bid=bid,
                                         edition=edition, authors=tempauthors)
    else:
        return flask.abort(404)


if __name__ == '__main__':
    app.run(debug=True)