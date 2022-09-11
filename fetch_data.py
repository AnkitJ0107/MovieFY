import requests
import pickle
import pandas as pd

movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))

def recommend(movie_title):
    movie_index = movies[movies["title"] == movie_title].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[
        1:13
    ]
    m_ids=[]
    for i in movies_list:
        m_id = movies.iloc[i[0]].movie_id
        m_ids.append(m_id)
    return m_ids

def fetch_poster(movie_id , movie_title):
        my_api_key = "40e9173d75720c58e466975159f997ce"
        response = requests.get(
            "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US".format(
                movie_id, my_api_key
            )
        )
        data = response.json()
        if data["poster_path"] == None:
            poster_path = "https://picsum.photos/500/750"
        else:
            poster_path = "https://image.tmdb.org/t/p/w185" + data["poster_path"]

        if data["overview"] == None:
            overview = "No Data"
        else:
            overview = data["overview"]

        if data["vote_average"] == None:
            vote_average = "No Data"
        else:
            vote_average = data["vote_average"]

        if data["release_date"] == None:
            release_date = "No Data"
        else:
            release_date = data["release_date"]
            release_year = release_date[:4]

        if data["runtime"] == None:
            runtime = "No Data"
        else:
            runtime= data["runtime"]
        
        if data["genres"] == None:
            genres = "No Data"
        else:
            genres= data["genres"]

        if data["imdb_id"] == None:
            imdb_id = "https://www.imdb.com/title/tt1762742"
        else:
            imdb_id = "https://www.imdb.com/title/" + data["imdb_id"]

        return movie_title, poster_path, overview, vote_average, imdb_id, release_year, runtime, genres