from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from fetch_data import fetch_poster, recommend
app = Flask(__name__)

genre=['Action', 'Adventure', 'Fantasy', 'Science Fiction', 'Crime', 'Drama', 'Thriller', 'Animation', 'Family',
 'Western', 'Comedy', 'Romance', 'Horror', 'Mystery', 'War', 'History', 'Music', 'Documentary', 'Foreign', 'TV Movie']
movies=pd.read_csv("tmdb_5000_movies.csv")

@app.route("/" , methods=["POST", "GET"])
def index():
    if request.method=="POST":
        name=request.form["search"]
        return redirect(url_for("movie_name" , name=name))
    else:
        return render_template('index.html', genre=genre, m_titles=movies.title)

@app.route("/<name>" , methods=["POST", "GET"])
def movie_name(name):
    for i in range(movies.shape[0]):
        if movies.iloc[i].title==name :
            mid=movies.iloc[i].id
            break 
    movie_title, poster_path, overview, vote_average, imdb_id, release_year, runtime, genres=fetch_poster(mid , name)
    m_ids=recommend(name)
    if request.method=="POST":
        name=request.form["search"]
        return redirect(url_for("movie_name" , name=name))
    else:
        return render_template('movie_home.html', movie_title=movie_title, poster_path=poster_path, overview=overview,
         rating=vote_average, imdb_id=imdb_id, m_titles=movies.title, genre=genre, m_ids=m_ids, release_year=release_year, runtime=runtime, genres=genres)

@app.route("/category/<name>" , methods=["POST", "GET"])
def category(name):
    p1="./dataset/"
    p2="_movies_data.csv"
    p=p1+name+p2
    movies_type=[]
    movies_type.append(pd.read_csv(p))
    if request.method=="POST":
        name=request.form["search"]
        return redirect(url_for("movie_name" , name=name))
    else:
        return render_template('category.html', genre=genre, name=name, m_id=movies_type[0]['movie_id'][:50], m_titles=movies.title)

if __name__ == "__main__":
    app.run(debug=True)