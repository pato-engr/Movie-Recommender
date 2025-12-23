import streamlit as st
import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 💾 Load movies dataset
movies = pickle.load(open('movies.pkl', 'rb'))

# 🔹 Prepare vectorizer
cv = CountVectorizer(max_features=2000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

# 🔹 Recommendation function (dynamic similarity)
def recommend(movie_name):
    movie_name = movie_name.strip().lower()
    titles = movies['title'].str.lower().str.strip()
    
    if movie_name not in titles.values:
        return []

    idx = titles[titles == movie_name].index[0]
    
    # Compute similarity dynamically
    movie_vector = vectors[idx].reshape(1, -1)
    similarity = cosine_similarity(movie_vector, vectors)[0]
    
    # Get top 5 similar movies
    similar_movies = sorted(list(enumerate(similarity)), key=lambda x: x[1], reverse=True)[1:6]
    return [movies.iloc[i[0]].title for i in similar_movies]

# 🖼️ Streamlit UI
st.set_page_config(page_title="Movie Recommender", layout="centered")
st.title("🎬 Movie Recommender System")
st.markdown("Type in a movie you like and get similar recommendations!")

movie_name = st.text_input("🔍 Enter a movie title or keyword:")

if st.button("Recommend"):
    recommendations = recommend(movie_name)
    
    if recommendations:
        st.subheader("✅ You may also like:")
        for title in recommendations:
            st.write(f"✅ {title}")
    else:
        st.error("❌ Movie not found. Try another title from TMDB 5000.")
