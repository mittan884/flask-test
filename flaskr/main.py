import re
import sqlite3

from flask import redirect, render_template, request, url_for

from flaskr import app
from flaskr.db import DATABASE

DATABASE = 'database.db'
var_lists = []


@app.route('/')
def index():
    con = sqlite3.connect(DATABASE)
    cursor = con.execute('SELECT * FROM books')

    column_list = list(column[0] for column in cursor.description)

    books = list(dict(zip(column_list, row)) for row in cursor)
    return render_template('index.html', books = books)


@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/kesu')
def kesu():
    con = sqlite3.connect(DATABASE)
    cursor = con.execute('SELECT * FROM books')

    column_list = list(column[0] for column in cursor.description)

    books = list(dict(zip(column_list, row)) for row in cursor)
    return render_template('kesu.html', books = books)

@app.route('/hennsyu')
def hennsyu():
    con = sqlite3.connect(DATABASE)
    cursor = con.execute('SELECT * FROM books')
    column_list = list(column[0] for column in cursor.description)
    column_list = list(column[0] for column in cursor.description)

    books = list(dict(zip(column_list, row)) for row in cursor)
    
    return render_template('hennsyu.html', books = books)
    


@app.route('/register', methods = ['POST'])
def register():
    while True:
        title = request.form['title']
        price = request.form['price']
        year = request.form['year']
        month = request.form['month']
        day = request.form['day']

        p = re.compile('[0-9]+')
        if all(map(p.fullmatch, (price, year, month, day))):
            break

    con = sqlite3.connect(DATABASE)
    con.execute(
        'INSERT INTO books VALUES(?,?,?,?,?)',
        [title, price, year, month, day]
    )
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
        con.execute('INSERT INTO books VALUES(?,?,?,?,?)', row)
    con.commit()
    con.close()

    return redirect(url_for('index'))

    
@app.route('/henkou', methods = ['POST'])
def henkou():
    # チェックボックスで選択された行番号
    row_num_list = request.form.getlist('selected_row')

    con = sqlite3.connect(DATABASE)
    db_books = con.execute('SELECT * FROM books').fetchall()

    # 選択されてないものだけを残す
    new_db_books = []
    for i, row in enumerate(db_books):

            new_db_books.append(row)

    # データベースの更新
    con.execute('DELETE FROM books')
    for row in new_db_books:
        
        cursor = con.execute(
        'UPDATE books SET 入荷日 = year, タイトル = title, 金額 = price WHERE id = column_list ',row
        )
    
    con.commit()
    con.close()

    return redirect(url_for('index'))
