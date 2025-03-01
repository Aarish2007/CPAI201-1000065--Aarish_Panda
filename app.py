import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import random
from PIL import Image

# Load the CSV file containing the product data
@st.cache_data
def load_data():
    df = pd.read_csv('data_output\product_details.csv')  # Replace with the correct path to your CSV file
    return df

# Preprocess the product data
@st.cache_data
def preprocess_data(df):
    df.fillna('', inplace=True)
    df['Price'] = df['Price'].str.replace(r'[^0-9]', '', regex=True).astype(int)
    df['combined'] = df['Category'] + " " + df['Brand'] + " " + df['Description']
    return df

# Train TF-IDF Vectorizer and calculate cosine similarity
@st.cache_resource
def train_model(df):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    with open('model_training\cosine_sim.pkl', 'wb') as f:
        pickle.dump(cosine_sim, f)
    with open('model_training\\tfidf.pkl', 'wb') as f:
        pickle.dump(tfidf, f)

    return tfidf, cosine_sim

# Load pre-trained model and TF-IDF vectorizer
@st.cache_resource
def load_model():
    with open('model_training\cosine_sim.pkl', 'rb') as f:
        cosine_sim = pickle.load(f)
    with open('model_training\\tfidf.pkl', 'rb') as f:
        tfidf = pickle.load(f)
    return tfidf, cosine_sim

# Recommend products based on user input
def recommend_products(user_input, price_range, rating_filter, brand_filter, category_filter, gender_filter, cosine_sim, df, tfidf):
    user_input_vector = tfidf.transform([user_input])
    user_input_sim = cosine_similarity(user_input_vector, tfidf.transform(df['combined']))
    similar_indices = user_input_sim.argsort()[0][::-1]

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

        if len(filtered_recommendations) >= 5:  # Limit to 5 recommendations
            break

    return filtered_recommendations

# Quiz game function
def play_quiz():
    questions = [
        {
            'question': 'What color is associated with elegance and luxury in fashion?',
            'options': ['Red', 'Blue', 'Black', 'Yellow'],
            'answer': 'Black'
        },
        {
            'question': 'Which accessory is considered a must-have for a fashion-conscious person?',
            'options': ['Hat', 'Sunglasses', 'Belt', 'Scarf'],
            'answer': 'Sunglasses'
        },
        {
            'question': 'What is the term used for clothing made from synthetic fibers?',
            'options': ['Cotton', 'Polyester', 'Denim', 'Silk'],
            'answer': 'Polyester'
        },
        {
            'question': 'Which brand is known for its luxury fashion?',
            'options': ['Nike', 'Gucci', 'Adidas', 'Zara'],
            'answer': 'Gucci'
        },
        {
            'question': 'Which season is considered the best for fashion trends?',
            'options': ['Summer', 'Winter', 'Fall', 'Spring'],
            'answer': 'Fall'
        }
    ]

    score = 0
    random.shuffle(questions)  # Shuffle questions for randomness
    for question in questions:
        answer = st.radio(question['question'], question['options'])
        if answer == question['answer']:
            score += 1

    return score

# Streamlit app
def main():
    st.set_page_config(page_title='Shophoria - Fashion Recommendations', page_icon='🛍️', layout='wide')

    # U-shaped filter and Shophoria logo
    #logo_path = "AARISH SIS/Shophira/images/logo.png"
    #st.sidebar.image(logo_path, width=200)
    st.sidebar.header("Shophoria Personalized Fashion Recommendation")
    
    # Suggestion box for playing the quiz game
    game_option = st.sidebar.selectbox("Do you want to play a game?", ["No", "Yes"])

    if game_option == "Yes":
        st.write("🎮 **Fashion Quiz**")
        score = play_quiz()
        st.write(f"📝 Your Score: {score} out of 5")
        
        # Display recommendations based on score
        if score == 5:
            st.write("🎉 You scored 5/5! Here are some top recommendations for you:")
        else:
            st.write(f"Better luck next time! You scored {score}/5. Here are some recommendations:")
        
        df = load_data()
        df = preprocess_data(df)
        
        try:
            tfidf, cosine_sim = load_model()
        except FileNotFoundError:
            tfidf, cosine_sim = train_model(df)

        # Get recommendations based on quiz score
        user_input = "fashion"
        price_range = (500, 2000)
        rating_filter = 4
        brand_filter = []
        category_filter = []
        gender_filter = None

        recommendations = recommend_products(user_input, price_range, rating_filter, brand_filter, category_filter, gender_filter, cosine_sim, df, tfidf)

        if recommendations:
            st.write("🎯 **Top Recommendations for You:**")
            row_count = 3
            recommendations = recommendations[:row_count * 3]
            rows = [recommendations[i:i + 3] for i in range(0, len(recommendations), 3)]

            for row in rows:
                cols = st.columns(3)
                for col, rec in zip(cols, row):
                    with col:
                        st.markdown(f"#### [View Product]({rec['product_link']})")
                        st.image(rec['image_url'], use_column_width='always')
                        st.markdown(
                            f"**Brand:** {rec['brand']}<br>"
                            f"**Category:** {rec['category']}<br>"
                            f"⭐ Rating: {rec['rating']}<br>"
                            f"💰 Price: ₹{rec['price']}",
                            unsafe_allow_html=True,
                        )

    elif game_option == "No":
        df = load_data()
        df = preprocess_data(df)

        try:
            tfidf, cosine_sim = load_model()
        except FileNotFoundError:
            tfidf, cosine_sim = train_model(df)

        # Search recommendation bar
        st.write("🔍 Enter a product description, brand, or category:")
        user_input = st.text_input("Search for Fashion Products")

        if user_input:
            recommendations = recommend_products(user_input, (500, 2000), 4, [], [], None, cosine_sim, df, tfidf)

            if recommendations:
                st.write("🎯 **Top Recommendations for You:**")
                row_count = 3
                recommendations = recommendations[:row_count * 3]
                rows = [recommendations[i:i + 3] for i in range(0, len(recommendations), 3)]

                for row in rows:
                    cols = st.columns(3)
                    for col, rec in zip(cols, row):
                        with col:
                            st.markdown(f"#### [View Product]({rec['product_link']})")
                            st.image(rec['image_url'], use_column_width='always')
                            st.markdown(
                                f"**Brand:** {rec['brand']}<br>"
                                f"**Category:** {rec['category']}<br>"
                                f"⭐ Rating: {rec['rating']}<br>"
                                f"💰 Price: ₹{rec['price']}",
                                unsafe_allow_html=True,
                            )
            else:
                st.warning("No products found matching your criteria. Try adjusting the filters or search terms.")

if __name__ == '__main__':
    main()
