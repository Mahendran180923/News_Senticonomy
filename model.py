# Import required packages
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import os
import joblib # Keep joblib if you use it elsewhere, otherwise it could be removed
import psycopg2
from datetime import datetime
from sqlalchemy import create_engine
import pickle # Import the pickle module for in-memory serialization

# --- NLTK Downloads (Corrected and robust check) ---
required_nltk_data = ['punkt', 'wordnet', 'stopwords', 'vader_lexicon']
for data_name in required_nltk_data:
    try:
        nltk.data.find(data_name)
        print(f"NLTK data '{data_name}' already downloaded.")
    except LookupError:
        print(f"NLTK data '{data_name}' not found. Downloading...")
        nltk.download(data_name)
        print(f"NLTK data '{data_name}' downloaded successfully.")


# --- Configuration Parameters ---
TFIDF_MAX_FEATURES = 5000
KMEANS_RANDOM_STATE = 42
KMEANS_N_INIT = 10

# PostgreSQL DB Connection Parameters
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "mdte16db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_PORT = os.getenv("DB_PORT", "5432")

DB_PROCESSED_DATA_TABLE_NAME = "news_data_processed"


# --- 1. Data Loading ---
try:
    df = pd.read_csv("cleaned_news_data.csv")
    if 'Unnamed: 0' in df.columns:
        df.drop(['Unnamed: 0'], axis=1, inplace=True)
    print("Data loaded successfully.")
    print(f"Initial DataFrame shape: {df.shape}")
    print(df.info())
    print("\nNull values after initial load:")
    print(df.isnull().sum())
    print("-" * 50)
except FileNotFoundError:
    print("Error: 'cleaned_news_data.csv' not found. Please ensure the file exists in the same directory.")
    exit()

# --- 2. Text Preprocessing for Clustering and Sentiment Analysis ---
df['headline'] = df['headline'].fillna('')
df['content'] = df['content'].fillna('')
df['category'] = df['category'].fillna('')

print("--- Starting Text Preprocessing ---")
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text_for_ml(text):
    if not isinstance(text, str):
        return ""
    words = word_tokenize(text)
    processed_words = [
        lemmatizer.lemmatize(word.lower())
        for word in words
        if word.lower() not in stop_words and word.isalpha()
    ]
    return ' '.join(processed_words)

df['full_text_for_clustering'] = df['category'] + " " + df['headline']
df['processed_text_for_clustering'] = df['full_text_for_clustering'].apply(preprocess_text_for_ml)

def clean_text_for_sentiment(text):
    if not isinstance(text, str):
        return ""
    words = word_tokenize(text)
    cleaned_words = [word.lower() for word in words if word.lower() not in stop_words]
    return ' '.join(cleaned_words)

df['cleaned_content_for_sentiment'] = df['content'].apply(clean_text_for_sentiment)

print("Text preprocessing complete.")
print("-" * 50)

# --- 3. Feature Extraction (Text Vectorization) ---
print("--- Starting Feature Extraction (TF-IDF) ---")
vectorizer = TfidfVectorizer(max_features=TFIDF_MAX_FEATURES)
document_vectors = vectorizer.fit_transform(df['processed_text_for_clustering'])

print(f"TF-IDF Vectorization complete. Document vectors shape: {document_vectors.shape}")
print("-" * 50)

# --- 4. Clustering (K-Means) ---
print("--- Starting K-Means Clustering ---")
no_of_clusters = len(df['category'].unique())
print(f"K-Means will attempt to form {no_of_clusters} clusters (based on unique 'category' labels).")

kmeans = KMeans(n_clusters=no_of_clusters, random_state=KMEANS_RANDOM_STATE, n_init=KMEANS_N_INIT)
df['cluster'] = kmeans.fit_predict(document_vectors)

inertia = kmeans.inertia_
print(f'K-Means Clustering complete. Model inertia: {inertia:.2f}')

print("\nK-Means Cluster Distribution:")
print(df['cluster'].value_counts().sort_index())
print("-" * 50)

# --- Store K-Means Model in PostgreSQL DB ---
print("--- Storing K-Means Model in PostgreSQL DB ---")
conn_model = None
cur_model = None
try:
    # Corrected Line: Use pickle.dumps() for in-memory serialization
    serialized_kmeans_model = pickle.dumps(kmeans)
    model_name = f"KMeans_Clustering_Model_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    conn_model = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    cur_model = conn_model.cursor()

    cur_model.execute("""
        CREATE TABLE IF NOT EXISTS ml_models (
            id SERIAL PRIMARY KEY,
            model_name VARCHAR(255) NOT NULL,
            model_data BYTEA NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn_model.commit()

    cur_model.execute(
        "INSERT INTO ml_models (model_name, model_data) VALUES (%s, %s);",
        (model_name, serialized_kmeans_model)
    )
    conn_model.commit()
    print(f"K-Means model '{model_name}' stored successfully in PostgreSQL.")

except psycopg2.Error as e:
    print(f"Error storing K-Means model in PostgreSQL: {e}")
    if conn_model:
        conn_model.rollback()
finally:
    if cur_model:
        cur_model.close()
    if conn_model:
        conn_model.close()
    print("-" * 50)


# --- 5. Sentiment Analysis ---
print("--- Starting Sentiment Analysis (VADER) ---")
sia = SentimentIntensityAnalyzer()

def calculate_sentiment_score(text):
    return sia.polarity_scores(text)

df['sentiment_scores'] = df['cleaned_content_for_sentiment'].apply(calculate_sentiment_score)

df['neg'] = df['sentiment_scores'].apply(lambda x: x['neg'])
df['neu'] = df['sentiment_scores'].apply(lambda x: x['neu'])
df['pos'] = df['sentiment_scores'].apply(lambda x: x['pos'])
df['compound'] = df['sentiment_scores'].apply(lambda x: x['compound'])

print("Sentiment analysis complete.")
print("-" * 50)

# --- 6. Final Data Cleaning and Push to PostgreSQL DB ---
print("--- Finalizing Data and Pushing to PostgreSQL DB ---")

columns_to_drop_final = [
    'web_url', 'time', 'day', 'month',
    'full_text_for_clustering', 'processed_text_for_clustering',
    'cleaned_content_for_sentiment', 'sentiment_scores'
]
df.drop(columns=columns_to_drop_final, axis=1, inplace=True, errors='ignore')

print("\nLast 50 rows of selected final columns:")
print(df[['category', 'headline', 'cluster', 'neg', 'neu', 'pos', 'compound']].tail(50))


# --- Push processed data to PostgreSQL DB ---
print(f"\n--- Pushing processed data to PostgreSQL DB table '{DB_PROCESSED_DATA_TABLE_NAME}' ---")
try:
    engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    df.to_sql(DB_PROCESSED_DATA_TABLE_NAME, engine, if_exists='replace', index=False)
    print(f"Processed data pushed to PostgreSQL table '{DB_PROCESSED_DATA_TABLE_NAME}' successfully.")

except Exception as e:
    print(f"Error pushing data to PostgreSQL: {e}")
finally:
    print("-" * 50)


print("\nScript execution finished.")
