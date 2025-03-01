# recommender.py
from sklearn.metrics.pairwise import cosine_similarity

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
