Shophoria - AI-Powered Fashion Recommendation System

📌 Introduction

Welcome to Shophoria, an AI-powered fashion recommendation system designed to help users find the best clothing and accessories based on their preferences. This project uses Machine Learning (ML) and Natural Language Processing (NLP) to analyze product descriptions and suggest relevant fashion items.

🌟 Key Features:

✔️ Personalized Recommendations – Get fashion suggestions based on user input.
✔️ Interactive Fashion Quiz – Answer questions to receive style-based recommendations.
✔️ AI-Powered Model – Uses text analysis to understand and find similar products.
✔️ Customizable Filters – Filter results based on price, rating, brand, and category.
✔️ User-Friendly Interface – Easy-to-use web platform for seamless shopping.

This capstone project demonstrates how AI can revolutionize the fashion industry, making shopping smarter, easier, and more enjoyable! 🛍️

🎯 Project Objectives

This project aims to:
✅ Create a smart recommendation system that suggests fashion items based on user input.
✅ Improve user experience with search filters (price, rating, brand, category, gender).
✅ Use AI to enhance recommendations by analyzing product descriptions with NLP.
✅ Make fashion discovery engaging by integrating a fun quiz-based approach.
✅ Scrape fashion product data from websites to keep the dataset updated.
✅ Develop a user-friendly web application with Streamlit for UI and Flask for backend processing.

🔧 Technologies & Tools Used

Technology

Purpose

Python

Core programming language

Pandas

Data manipulation and preprocessing

NumPy

Numerical computations

Scikit-learn

Machine Learning (TF-IDF, Cosine Similarity)

Flask

Backend API to run the model

Streamlit

Front-end interface for user interaction

BeautifulSoup & Requests

Web scraping to gather product data

Pickle

Saving and loading the trained models

HTML/CSS

Creating a structured recommendation page

📂 Project Structure

Shophoria-Capstone
│── app.py                    # Main Streamlit application
│── data_loader.py            # Loads & preprocesses product data
│── model.py                  # Machine Learning model (TF-IDF & Cosine Similarity)
│── recommender.py            # Core recommendation logic
│── PyBacked_Rec.py           # Flask API to start Streamlit
│── test.py                   # Testing the recommendation system
│── recommendations.html      # Web-based recommendation display
│── data/
│   ├── fashion_qna.csv       # Fashion-based Q&A dataset
│   ├── product_details.csv   # Product dataset from web scraping
│── model_training/
│   ├── cosine_sim.pkl        # Saved Cosine Similarity model
│   ├── tfidf.pkl             # Saved TF-IDF vectorizer
│── web_scraping_scripts/     # Scripts for scraping fashion product data

🏗️ How the System Works

1️⃣ Collecting & Preprocessing Data

Fashion product data is gathered from e-commerce websites via web scraping.

Preprocessing steps:

Remove missing values.

Convert price values to a numeric format.

Merge product description, brand, and category into a single text field.

Store the cleaned data for efficient processing.

2️⃣ Training the AI Model

The system uses TF-IDF (Term Frequency-Inverse Document Frequency) to convert product descriptions into numerical values.

Cosine Similarity is applied to measure how similar a user’s input is to products in the dataset.

The trained model and similarity matrix are saved so they don’t need to be recomputed every time.

3️⃣ Generating Personalized Recommendations

The user inputs a product name, brand, or category (e.g., "black leather jacket").

The system finds similar products based on:

Price Range – Users can set a custom range (e.g., ₹500 - ₹2000).

Minimum Rating – Filters items with ratings above a chosen threshold (e.g., 4 stars).

Preferred Brands & Categories – Users can select specific brands (Nike, Adidas, etc.).

Gender Filter – Users can choose recommendations for Men, Women, or Unisex.

The system displays top 5 product recommendations with images, prices, ratings, and links.

4️⃣ User-Friendly Web Interface

Built using Streamlit, the interface offers:

A search bar for product discovery.

Dropdown menus & sliders for filtering results.

Interactive product displays with images and direct shopping links.

5️⃣ Fashion Quiz Feature 🎮

A 5-question quiz helps determine the user’s fashion style.

Users receive recommendations based on their quiz score.

Sample questions:

What color represents elegance? (Answer: Black)

Which brand is known for luxury fashion? (Answer: Gucci)

🚀 How to Run the Project

Step 1️⃣: Install Dependencies

Ensure Python (≥3.8) is installed, then run:

pip install -r requirements.txt

Step 2️⃣: Start the Backend Server

python PyBacked_Rec.py

Step 3️⃣: Launch the Web Application

streamlit run app.py

Step 4️⃣: Open in Your Browser

Go to http://localhost:8501 to start using Shophoria.

📌 Future Enhancements

🔹 Advanced AI Models – Upgrade to BERT or Transformer-based NLP models.
🔹 More Personalization – Improve recommendations with user profiles and saved preferences.
🔹 E-commerce Integration – Connect directly to Myntra, Amazon, and Flipkart APIs.
🔹 Better Product Filters – Add features like fabric type, occasion-based suggestions, and trending styles.

🏆 Conclusion

Shophoria is an AI-driven fashion assistant that makes online shopping smarter and more enjoyable. With its blend of Machine Learning, Web Scraping, and Interactive UI, it provides a seamless and intelligent shopping experience.

🛍️ Discover Your Style with Shophoria! 🎉


Here are the working screenshots that I have attateched below:- 
![Screenshot 2025-02-28 121652](https://github.com/user-attachments/assets/da989c6e-5f08-4aa1-a049-4d200ad87ec2)
![Screenshot 2025-02-28 125152](https://github.com/user-attachments/assets/5525cdc2-7c47-468b-9f79-df8aeb3fc668)
![Screenshot 2025-02-28 122116](https://github.com/user-attachments/assets/ac98724e-b573-48e9-8699-7e75054ffe54)
![Screenshot 2025-02-28 125205](https://github.com/user-attachments/assets/829daf46-f2b6-4ad7-b18c-8827a812bdf1)


