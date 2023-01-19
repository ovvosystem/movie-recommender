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
        search_titles = db.execute("SELECT title FROM movies JOIN ratings ON movies.movieId = ratings.movieId WHERE ratings.userId IN (SELECT userId FROM ratings JOIN movies ON ratings.movieId = movies.movieId WHERE movies.title = ? AND ratings.rating > 4) AND ratings.rating > 4 AND NOT movies.title = ?", (movie, movie,)).fetchall()
        search_ratings = db.execute("SELECT rating FROM ratings JOIN movies ON ratings.movieId = movies.movieId WHERE ratings.userId IN (SELECT userId FROM ratings JOIN movies ON ratings.movieId = movies.movieId WHERE movies.title = ? AND ratings.rating > 4) AND ratings.rating > 4 AND NOT movies.title = ?", (movie, movie,)).fetchall()
        
        titles = pd.Series(search_titles)
        ratings = pd.Series(search_ratings)
        
        search_group = {}
        
        for i in range(len(titles)):
            if titles[i] in search_group:
                search_group[titles[i]] += [ratings[i]]
            else:
                search_group[titles[i]] = [ratings[i]]
                
        result = {}
                
        for key in search_group:
            total_ratings = db.execute("SELECT count(rating) FROM ratings JOIN movies ON ratings.movieId = movies.movieId WHERE movies.title = ? AND ratings.rating > 4", (key,)).fetchone()
            if total_ratings > 10:
                group_ratings = len(search_group[key])
                result[key] = group_ratings / total_ratings
            
        recommendations = pd.DataFrame(list(result.items()), columns=['title','percent'])
        test = recommendations.sort_values(by=['percent'], ascending=False).head()
        
        return render_template("test.html", test=test)
        
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)