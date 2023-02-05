import pickle
import pandas as pd

class Movie:
    @classmethod
    def movies():
        movie_list = pickle.load(open('./model/movies_data.pkl', 'rb'))
        movies = pd.DataFrame(movie_list)
        print(movies.head())
        return movies
