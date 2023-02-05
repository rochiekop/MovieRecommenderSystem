import streamlit as st
import pickle
import pandas as pd
import requests
import const as const
from ui.apperance import do_stuff_on_page_load


do_stuff_on_page_load(const.TYPE_SCREEN)

movie_list = pickle.load(open('./model/movies_data.pkl', 'rb'))
movies = pd.DataFrame(movie_list)


recommended_movie_num = st.sidebar.slider(
    "Recommended movie number", min_value=5, max_value=10)
if recommended_movie_num:
    const.MOVIE_NUMBER = recommended_movie_num


def recommendation(movie_name):
    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),
                         reverse=True, key=lambda x: x[1])[0:const.MOVIE_NUMBER]
    result_recommendation = []
    result_recommendation_img = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        result_recommendation_img.append(fetch_poster(movie_id))
        result_recommendation.append(movies.iloc[i[0]].title)
    return result_recommendation, result_recommendation_img


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c2fe302d9b35017bd00852d79c7177a2".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


similarity = pickle.load(open('./model/similarity.pkl', 'rb'))


st.title('Example of Recommender System (Search Movies)')
option = st.selectbox(
    'How would you like to be search?',
    movies['title'])


cols = st.columns(const.MOVIE_NUMBER)
if st.button('Search'):
    with st.spinner('Find The Movies...'):
        recommended_movie_names, recommended_movie_img = recommendation(option)
        for i, x in enumerate(cols):
            with x:
                st.image(recommended_movie_img[i])
                st.text(recommended_movie_names[i])
