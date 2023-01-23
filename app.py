from flask import Flask, render_template, request
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
        
        search_group = {}
        
        for i in range(len(search_titles)):
            if search_titles[i] in search_group:
                search_group[search_titles[i]] += [search_ratings[i]]
            else:
                search_group[search_titles[i]] = [search_ratings[i]]
            
        result = {}
                
        for key in search_group:
            total_ratings = db.execute("SELECT SUM(rating) FROM ratings JOIN movies ON ratings.movieId = movies.movieId WHERE movies.title = ? AND ratings.rating > 4", (key,)).fetchone()
            if total_ratings > 10:
                group_ratings = sum(search_group[key])
                result[key] = group_ratings / total_ratings
            
        recommendations = pd.DataFrame(list(result.items()), columns=['title','percent'])
        top5 = recommendations.sort_values(by=['percent'], ascending=False).head()
        
        return render_template("recommendations.html", recommendations=top5)
    
    all_titles = db.execute("SELECT title FROM movies").fetchall()
        
    return render_template("index.html", movies=all_titles)

if __name__ == "__main__":
    app.run(debug=True)