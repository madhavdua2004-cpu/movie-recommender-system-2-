import streamlit as st
import pickle
import pandas as pd
import requests


# ----------------- Helper Function ----------------- #
def fetch_poster(movie_id):
    # Call TMDB API to get movie details. Be defensive: network errors or
    # missing 'poster_path' should not crash the app.
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=c1ca0b6a67af6cfea30184830a10742c&language=en-US',
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
    except Exception:
        # On any error (network, non-200, JSON decode), return a placeholder image.
        return 'https://via.placeholder.com/500x750?text=No+Image'

    poster_path = data.get('poster_path')
    if poster_path:
        return 'https://image.tmdb.org/t/p/original' + data ['poster_path']



# ----------------- Recommendation Function ----------------- #
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


# ----------------- Load Data ----------------- #
movies_dict = pickle.load(open('movie.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ----------------- Streamlit UI ----------------- #
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
