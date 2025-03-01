# model.py
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

@st.cache_resource
def train_model(df):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined'])

    # Calculate cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Save the model and TF-IDF vectorizer
    with open('model_training\cosine_sim.pkl', 'wb') as f:
        pickle.dump(cosine_sim, f)
    with open('model_training\\tfidf.pkl', 'wb') as f:
        pickle.dump(tfidf, f)

    return tfidf, cosine_sim

@st.cache_resource
def load_model():
    with open('model_training\cosine_sim.pkl', 'rb') as f:
        cosine_sim = pickle.load(f)
    with open('model_training\\tfidf.pkl', 'rb') as f:
        tfidf = pickle.load(f)
    return tfidf, cosine_sim
