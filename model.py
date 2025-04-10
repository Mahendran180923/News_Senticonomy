# Import required packages
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import download
from sklearn.cluster import KMeans
from transformers import pipeline
from textblob import TextBlob
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os


download('punkt')
download('wordnet')
download('stopwords')

df = pd.read_csv("cleaned_news_data.csv")

vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
x = vectorizer.fit_transform(df['category']+ " "+df['headline'] )

no_of_clusters = len(df['category'].unique())
# print(f"The number of clusers is: {no_of_clusters}")

kmeans = KMeans(n_clusters=no_of_clusters, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(x)


unique_cluster, counts = np.unique(df['cluster'], return_counts=True)

# for cluster, count in zip(unique_cluster, counts):
#     print(f"{cluster}: {count}")

inertia = kmeans.inertia_

print(f'The model inertia is: {inertia}')
# print(df.isnull().sum())
# print(df.info())

df = df.copy()
df.drop(['Unnamed: 0'], axis=1, inplace=True)

nltk.download('vader_lexicon')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

sia = SentimentIntensityAnalyzer()

def process_text(text):
    # Tokenize the text into words
    words = word_tokenize(text)

    # Remove stop words and lemmatize the words
    words = [lemmatizer.lemmatize(word.lower()) for word in words if word.lower() not in stop_words]
    return ' '.join(words)

def calculate_sentiment_score(text):
    sentiment_score = sia.polarity_scores(text)
    return sentiment_score

df['processed_content'] = df['content'].apply(process_text)


df['sentiment_score'] = df['processed_content'].apply(calculate_sentiment_score)

df['neg'] = df['sentiment_score'].apply(lambda x: x['neg'])
df['neu'] = df['sentiment_score'].apply(lambda x: x['neu'])
df['pos'] = df['sentiment_score'].apply(lambda x: x['pos'])
df['compound'] = df['sentiment_score'].apply(lambda x: x['compound'])

df.drop(['sentiment_score', 'processed_content'], axis=1, inplace=True)

print(df[['category', 'cluster', 'neg', 'neu', 'pos', 'compound']].tail(50))

df.drop(['web_url', 'time', 'day', 'month'], axis=1, inplace=True)

df.to_csv("final_data.csv")

new_df = pd.read_csv("final_data.csv")

print(new_df.info())
print(new_df.isnull().sum())


file_size = os.path.getsize('final_data.csv')

if file_size < 1024:
    print(f"The size of the CSV file is: {file_size} bytes")
elif file_size < 1024 ** 2:
    print(f"The size of the CSV file is: {file_size / 1024:.2f} KB")
else:
    print(f"The size of the CSV file is: {file_size / (1024 ** 2):.2f} MB")