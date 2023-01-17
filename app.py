from flask import Flask, render_template, url_for, request
import sqlite3
import pandas as pd

app = Flask(__name__)

def db_connection():
    conn = sqlite3.connect('movies.db')
    conn.row_factory = lambda cursor, row: row[0]
    return conn


@app.route('/', methods=['GET', 'POST'])
def index():
    conn = db_connection()
    db = conn.cursor()
    
    if request.method == 'POST':
        movie = request.form['movie']
        test = db.execute("SELECT title FROM movies WHERE title LIKE ?", (f'%{movie}%',)).fetchall()
        
        return render_template("test.html", test=test)
        
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)