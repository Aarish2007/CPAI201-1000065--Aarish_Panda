import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Load the CSV file containing the product data
@st.cache_data
def load_data():
    df = pd.read_csv('data_output/product_details.csv')  # Replace with the correct path to your CSV file
    return df

# Preprocess the product data
@st.cache_data
def preprocess_data(df):
    # Fill missing values
    df.fillna('', inplace=True)

    # Clean and convert the Price column to numeric
    df['Price'] = df['Price'].str.replace(r'[^0-9]', '', regex=True).astype(int)

    # Combine relevant fields for recommendation
    df['combined'] = df['Category'] + " " + df['Brand'] + " " + df['Description']

    # Save preprocessed data (optional for debugging or future use)
    df.to_csv('data_preprocessing/preprocessed_data.csv', index=False)
    return df

# Train TF-IDF Vectorizer and calculate cosine similarity
@st.cache_resource
def train_model(df):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined'])

    # Calculate cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Save the model and TF-IDF vectorizer
    with open('model_training/cosine_sim.pkl', 'wb') as f:
        pickle.dump(cosine_sim, f)
    with open('model_training/tfidf.pkl', 'wb') as f:
        pickle.dump(tfidf, f)

    return tfidf, cosine_sim

# Load pre-trained model and TF-IDF vectorizer
@st.cache_resource
def load_model():
    with open('model_training/cosine_sim.pkl', 'rb') as f:
        cosine_sim = pickle.load(f)
    with open('model_training/tfidf.pkl', 'rb') as f:
        tfidf = pickle.load(f)
    return tfidf, cosine_sim

# Recommend products based on user input
def recommend_products(user_input, price_range, rating_filter, brand_filter, category_filter, gender_filter, cosine_sim, df, tfidf):
    user_input_vector = tfidf.transform([user_input])
    user_input_sim = cosine_similarity(user_input_vector, tfidf.transform(df['combined']))
    similar_indices = user_input_sim.argsort()[0][::-1]

    # Filter products
    filtered_recommendations = []
    for i in similar_indices:
        product = df.iloc[i]
        if (price_range[0] <= product['Price'] <= price_range[1] and
            (rating_filter is None or product['Ratings'] >= rating_filter) and
            (not brand_filter or product['Brand'] in brand_filter) and
            (not category_filter or product['Category'] in category_filter) and
            (not gender_filter or product['Gender'] == gender_filter)):

            filtered_recommendations.append({
                'product_link': product['Product Link'],
                'image_url': product['Image URL'],
                'rating': product['Ratings'],
                'price': product['Price'],
                'brand': product['Brand'],
                'category': product['Category']
            })

        if len(filtered_recommendations) >= 5:
            break

    return filtered_recommendations

# Streamlit app
def main():
    st.set_page_config(page_title='Fashion Product Recommendation', page_icon='🛍️', layout='wide')
    st.markdown("<h1 style='font-size: 36px; text-align: center;'>🛍️ Fashion Product Recommendation System</h1>", unsafe_allow_html=True)

    df = load_data()
    df = preprocess_data(df)

    try:
        tfidf, cosine_sim = load_model()
    except FileNotFoundError:
        st.write("Training the model...")
        tfidf, cosine_sim = train_model(df)

    with st.sidebar:
        st.markdown("<h2>🔧 Filters</h2>", unsafe_allow_html=True)

        min_price, max_price = st.slider(
            "💸 Select Price Range (₹)", 
            min_value=int(df['Price'].min()), 
            max_value=int(df['Price'].max()), 
            value=(int(df['Price'].min()), int(df['Price'].max()))
        )

        rating_filter = st.slider("⭐ Minimum Rating", 0, 5, 0)

        brand_filter = st.multiselect("🏷️ Select Brand(s)", options=df['Brand'].unique(), default=[])

        category_filter = st.multiselect("📂 Select Category(ies)", options=df['Category'].unique(), default=[])

        gender_filter = st.radio("👔 Select Gender", options=[None, 'M', 'F'], format_func=lambda x: 'All' if x is None else ('Men' if x == 'M' else 'Women'))

    user_input = st.text_input("🔍 Enter a product description, brand, or category:")

    if user_input:
        recommendations = recommend_products(user_input, (min_price, max_price), rating_filter, brand_filter, category_filter, gender_filter, cosine_sim, df, tfidf)

        if recommendations:
            st.markdown("<h2>🎯 Top Recommendations for You:</h2>", unsafe_allow_html=True)
            for rec in recommendations:
                st.markdown(f"<h3><a href='{rec['product_link']}' target='_blank'>View Product</a></h3>", unsafe_allow_html=True)
                st.image(rec['image_url'], width=200)
                st.write(f"<p style='font-size: 18px;'><strong>Brand:</strong> {rec['brand']} | <strong>Category:</strong> {rec['category']} | ⭐ <strong>Rating:</strong> {rec['rating']} | 💰 <strong>Price:</strong> ₹{rec['price']}</p>", unsafe_allow_html=True)
                st.markdown("<hr>", unsafe_allow_html=True)
        else:
            st.warning("No products found matching your criteria. Try adjusting the filters or search terms.")

# Run the Streamlit app
if __name__ == '__main__':
    main()
