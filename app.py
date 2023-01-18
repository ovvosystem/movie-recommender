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
        search_group = db.execute("SELECT title FROM movies JOIN ratings ON movies.movieId = ratings.movieId WHERE ratings.userId IN (SELECT userId FROM ratings JOIN movies ON ratings.movieId = movies.movieId WHERE movies.title = ? AND ratings.rating > 4) AND ratings.rating > 4 AND NOT movies.title = ?", (f'{movie}', f'{movie}',)).fetchall()
        all_elements = pd.Series(search_group)
        test = pd.Series(all_elements.value_counts().head().index)
        
        return render_template("test.html", test=test)
        
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)