import sqlite3
from importlib.resources import read_text
from turtle import title

from flask import redirect, render_template, request, url_for

from flaskr import app
from flaskr.db import DATABASE

DATABASE = 'database.db'
var_lists = []


@app.route('/')
def index():
    con = sqlite3.connect(DATABASE)
    db_books = con.execute('SELECT * FROM books').fetchall()
    con.close()

    books = []
    for row in db_books:
        books.append({'title': row[0], 'price': row[1], 'arrival_day': row[2]})
    return render_template('index.html', books = books)


@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/kesu')
def kesu():
    con = sqlite3.connect(DATABASE)
    db_books = con.execute('SELECT * FROM books').fetchall()
    con.close()

    books = []
    for row in db_books:
        books.append({'title': row[0], 'price': row[1], 'arrival_day': row[2]})
    return render_template('kesu.html', books = books)


@app.route('/register', methods = ['POST'])
def register():
    title = request.form['title']
    price = request.form['price']
    arrival_day = request.form['arrival_day']

    con = sqlite3.connect(DATABASE)
    con.execute('INSERT INTO books VALUES(?,?,?)', [title, price, arrival_day])
    con.commit()
    con.close()
    return redirect(url_for('index'))


@app.route('/sakujyo', methods = ['POST'])
def sakujyo():
    # チェックボックスで選択された行番号
    row_num_list = request.form.getlist('selected_row')

    con = sqlite3.connect(DATABASE)
    db_books = con.execute('SELECT * FROM books').fetchall()

    # 選択されてないものだけを残す
    new_db_books = []
    for i, row in enumerate(db_books):
        if str(i) not in row_num_list:
            new_db_books.append(row)

    # データベースの更新
    con.execute('DELETE FROM books')
    for row in new_db_books:
        con.execute('INSERT INTO books VALUES(?,?,?)', row)
    con.commit()
    con.close()

    return redirect(url_for('index'))
