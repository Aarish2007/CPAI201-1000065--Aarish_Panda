# data_loader.py
import pandas as pd



def load_data():
    df = pd.read_csv('data_output\product_details.csv')  # Replace with the correct path to your CSV file
    return df


def preprocess_data(df):
    # Fill missing values
    df.fillna('', inplace=True)

    # Clean and convert the Price column to numeric
    df['Price'] = df['Price'].str.replace(r'[^0-9]', '', regex=True).astype(int)

    # Combine relevant fields for recommendation
    df['combined'] = df['Category'] + " " + df['Brand'] + " " + df['Description']

    # Save preprocessed data (optional for debugging or future use)
    df.to_csv('data_preprocessing\preprocessed_data.csv', index=False)
    print('data preprocessing done')
    return df
