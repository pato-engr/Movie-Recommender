

import streamlit as st
import pickle
import pandas as pd

import gzip

# 💾 Load the pre-processed movie data and similarity matrix
movies = pickle.load(open('movies.pkl', 'rb'))
with gzip.open("similarity.pkl.gz", "rb") as f:
    similarity = pickle.load(f)

# 🎯 Movie recommendation function
def recommend(movie_name):
    movie_name = movie_name.strip().lower()
    titles = movies['title'].str.lower().str.strip() 

    # 🔍 Check if movie exists
    if movie_name not in titles.values:
        return []

    # 🔢 Get index of the movie
    idx = titles[titles == movie_name].index[0]

    # 🚫 Safety check: out-of-bounds error
    if idx >= len(similarity):
        return []

    # 📈 Get most similar movies
    distances = list(enumerate(similarity[idx]))
    sorted_movies = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]

    recommended_titles = []
    for i in sorted_movies:
        if i[0] < len(movies):
            recommended_titles.append(movies.iloc[i[0]].title)

    return recommended_titles

# 🖼️ Streamlit UI
st.set_page_config(page_title="Movie Recommender", layout="centered")

st.title("🎬 Movie Recommender System")
st.markdown("Type in a movie you like and get similar recommendations!")

# 📥 Movie name input
movie_name = st.text_input("🔍 Enter a movie title or keyword:")

# 🧠 Recommend button
if st.button("Recommend"):
    recommendations = recommend(movie_name)
    
    if recommendations:
        st.subheader("✅ You may also like:")
        for title in recommendations:
            st.write(f"✅ {title}")
    else:
        st.error("❌ Movie not found. Try another title from TMDB 5000.")
