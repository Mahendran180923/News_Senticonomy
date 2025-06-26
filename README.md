# 📰 News Sentiment Analysis & Clustering Dashboard

![Overall Dashboard View with Filters](http://googleusercontent.com/run-storage/uploaded:Screenshot%202025-06-24%20014019.png-b2ebb794-7156-4bec-94a7-374960063027)

## 🚀 Project Overview

This project provides an end-to-end pipeline for **News Sentiment Analysis and Clustering**, guiding you from raw data acquisition to an interactive, insightful dashboard. The process meticulously covers:

1.  **Collecting raw news article data** from a public dataset.
2.  **Filtering** this data to a specific date range (2015-2024).
3.  **Creating a filtered CSV file and backing it up to an AWS S3 bucket.**
4.  **Downloading this filtered data from S3** for subsequent cleaning and text preprocessing.
5.  **Developing machine learning models** for content understanding.
6.  **Calculating sentiment scores** and persisting all processed data and models into a PostgreSQL database.
7.  **Building an insightful Streamlit dashboard** for interactive exploration of news sentiment and article clusters.

---

## ✨ Features

-   🤖 **Raw Data Collection:** Automates the collection of a large news article dataset from Kaggle.
-   ⏳ **Date Filtering:** Filters the collected raw data to include articles from 2015 to 2024.
-   ☁️ **AWS S3 Backup & Retrieval:** Securely backs up the filtered raw data to an S3 bucket and allows for easy retrieval for further processing.
-   🧼 **Robust Data Cleaning:** Handles missing values, extracts key information (dates, headlines), and filters articles by relevant categories and dates.
-   📝 **Text Preprocessing:** Utilizes NLTK for essential text operations including tokenization, lemmatization, and stopword removal to prepare content for analysis.
-   📈 **Feature Extraction:** Transforms textual content into numerical vectors using TF-IDF, making it suitable for machine learning algorithms.
-   🔎 **K-Means Clustering:** Groups similar news articles into distinct clusters based on their extracted content features.
-   😄 **VADER Sentiment Analysis:** Accurately calculates detailed polarity scores (negative, neutral, positive, and compound) for each news article.
-   🗃️ **PostgreSQL Integration:** Stores all processed news data (with sentiment and cluster information) and trained machine learning models for persistent, efficient access by the dashboard.
-   🌐 **Interactive Streamlit Dashboard:** Provides a user-friendly interface with:
    -   **Global Filters:** Apply selections for date range, news category, and article cluster to refine insights.
    -   **Filtered Data Table:** View a summary of articles based on your global filter selections.
        ![Interactive Filtered Data Table](Screenshot%202025-06-24%20013734.png)
    -   **Sentiment Trends & Distribution:**
        -   **Overall Sentiment Trend by Category:** Track the average sentiment score for each news category over time.
            ![Overall Sentiment Trend by Category](http://googleusercontent.com/run-storage/uploaded:Screenshot%202025-06-24%20013852.png-d68b97ec-5326-4cce-864d-08e732fec8ad)
        -   **Sentiment Trend (Year/Month-wise):** Compare category sentiment across selected years and months.
            ![Sentiment Trend (Year/Month-wise)](http://googleusercontent.com/run-storage/uploaded:Screenshot%2025-06-24%20013839.png-686e0a2f-a7d9-4dd8-9e2f-e38c2e7cbd33)
        -   **Sentiment Trend (Year/Quarter-wise):** Compare category sentiment across selected years and quarters.
            ![Sentiment Trend (Year/Quarter-wise)](http://googleusercontent.com/run-storage/uploaded:Screenshot%202025-06-24%20014056.png-6acf7e16-d78b-478a-9efa-536bea466e69)
        -   **Category-wise Sentiment Bar Chart:** Visualize the average sentiment score for each category across selected years.
            ![Category-wise Sentiment Bar Chart](http://googleusercontent.com/run-storage/uploaded:Screenshot%202025-06-24%20013805.png-c81aa090-b866-4565-a6be-01f25eafbea8)
        -   **Category Sentiment (Month/Year Comparison):** Compare sentiment trends for specific categories across different months and years.
            ![Category Sentiment (Month/Year Comparison)](http://googleusercontent.com/run-storage/uploaded:Screenshot%2025-06-24%20014117.png-9c3099f8-4f36-4cc3-9a91-09a58963ecde)
        -   **Sentiment Score Distribution:** Explore the distribution of sentiment scores by category or cluster.
            ![Sentiment Score Distribution](http://googleusercontent.com/run-storage/uploaded:Screenshot%202025-06-24%20013959.png-b795020b-8ac6-4e21-9373-ab0632415ea8)
        -   **News Volume Trend:** Analyze the daily or weekly volume of news articles.
            ![Daily/Weekly News Volume Trend](http://googleusercontent.com/run-storage/uploaded:Screenshot%202025-06-24%20013824.png-d076dda0-ab11-4237-99ab-69de4270bc6c)
        -   **Sentiment Extremes (Min/Max):** Track the minimum (most negative) and maximum (most positive) sentiment scores over time.
    -   **Word Clouds:**
        -   **Word Cloud by Cluster:** Visualize the most frequent words in headlines for each identified cluster.
            ![Word Cloud by Cluster](http://googleusercontent.com/run-storage/uploaded:Screenshot%202025-06-24%20013909.png-8689ca00-9c7a-4a23-b838-d5c90dff8dc8)
        -   **Sentiment Word Cloud (Positive/Negative/Neutral):** Explore words associated with positive, negative, and neutral sentiments for a selected year.
            ![Sentiment Word Cloud](http://googleusercontent.com/run-storage/uploaded:Screenshot%202025-06-24%20014040.png-b2ebb794-7156-4bec-94a7-374960063027)
    -   **Category-Cluster Comparison:**
        -   **Heatmap of Category vs. Cluster Counts:** A dense overview of the counts for each Category-Cluster pair.
            ![Heatmap of Category vs. Cluster Counts](http://googleusercontent.com/run-storage/uploaded:Screenshot%202025-06-24%20013925.png-1efe8366-8208-4aab-ba75-b41afa6c7b6a)
        -   Category-Cluster Comparison Tables.
    -   **Top N Articles by Sentiment:** View the most positive or most negative articles based on current filters.
        ![Top N Articles by Sentiment](http://googleusercontent.com/run-storage/uploaded:Screenshot%202025-06-24%20013940.png-527afd41-ec99-426d-8bdc-7a7cb4f9a089)

---

## 🗄️ Data Source

The project utilizes the "NYT Articles (21M+, 2000-Present)" dataset available on Kaggle.
To download, use the Kaggle CLI command: `kaggle datasets download -d aryansingh0909/nyt-articles-21m-2000-present`

## ⚙️ Prerequisites

Before running the project, ensure you have the following installed:

* **Python 3.8+**
* **PostgreSQL Database:** A running PostgreSQL instance is required to store the processed data and the ML model.
* **AWS Account:** For utilizing S3 for raw data storage and retrieval.
* **Kaggle API Key:** To download the dataset programmatically if you prefer not to download it manually.

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows: .\venv\Scripts\activate
    ```

3.  **Install Python dependencies:**
    Create a `requirements.txt` file in your project root with the following packages:
    ```
    pandas
    numpy
    scikit-learn
    matplotlib
    wordcloud
    nltk
    psycopg2-binary
    sqlalchemy
    plotly
    seaborn
    streamlit
    boto3
    python-dateutil
    pytz
    joblib
    ```
    Then install them:
    ```bash
    pip install -r requirements.txt
    ```

4.  **NLTK Data Downloads:**
    The `model.py` script automatically checks and downloads necessary NLTK data (`punkt`, `wordnet`, `stopwords`, `vader_lexicon`) when run.

---

## 🔐 Configuration

1.  **AWS Credentials (`.vscode/secrets.json`):**
    If you plan to use AWS S3 for data storage, create a `.vscode` directory in your project root and inside it, create a `secrets.json` file with your AWS Access Key and Secret Key:
    ```json
    {
        "AWS_ACCESS_KEY": "YOUR_AWS_ACCESS_KEY",
        "AWS_SECRET_KEY": "YOUR_AWS_SECRET_KEY"
    }
    ```
    > ⚠️ *Do NOT commit this file to public repos! Consider using environment variables or AWS Secrets Manager for production environments.*

2.  **PostgreSQL Credentials:**
    The Python scripts use environment variables for PostgreSQL connection details. Set the following environment variables:
    ```bash
    export DB_HOST="your_db_host" # e.g., localhost
    export DB_NAME="your_database_name" # e.g., mdte16db
    export DB_USER="your_username" # e.g., postgres
    export DB_PASSWORD="your_password"
    export DB_PORT="5432" # Default PostgreSQL port
    ```
    Ensure your PostgreSQL database (e.g., `mdte16db`) exists and your user has the necessary permissions.

---

## ▶️ Usage - Step-by-Step Pipeline

Follow these steps to run the complete news sentiment analysis and clustering pipeline:

1.  **Collect and Filter Raw Data:**
    Download the dataset from Kaggle manually or using the Kaggle CLI, and place `nyt-articles-21m-2000-present.zip` in the project root. Then execute `data_collection.py` which will collect and filter the raw data for the period 2015-2024.
    ```bash
    python data_collection.py
    ```

2.  **Upload Filtered Data to AWS S3 (Backup):**
    This step creates a `raw_data.csv` file with the filtered data and uploads it to your configured AWS S3 bucket for backup purposes.
    ```bash
    python aws_upload.py
    ```

3.  **Download Data from AWS S3 for Processing:**
    Retrieve the `raw_data.csv` from your S3 bucket. This file will then be used as input for the data cleaning and subsequent steps.
    ```bash
    python aws.download.py
    ```

4.  **Perform Data Cleaning & Preprocessing:**
    This script processes the downloaded `raw_data.csv` to clean the data and prepare it for model development.
    ```bash
    python data_cleaning.py
    ```

5.  **Develop Models, Calculate Sentiment, and Store in DB:**
    This script performs crucial steps including text preprocessing, K-Means clustering, and VADER sentiment analysis. It then pushes the final processed data, along with sentiment scores and cluster assignments, to the PostgreSQL table `news_data_processed`. It also stores the trained machine learning models in the `ml_models` database table.
    ```bash
    python model.py
    ```

6.  **Launch the Insightful Dashboard!**
    Start the interactive Streamlit dashboard to visualize and explore the news sentiment and article clusters.
    ```bash
    streamlit run data_visualisation.py
    ```

---

## 🗄️ Database Schema

-   **`news_data_processed`**: Table storing cleaned, enriched news articles with sentiment and cluster information.
    -   `date` (DATE): Date of the news article.
    -   `category` (TEXT): Category of the news article (e.g., 'Technology', 'Sports').
    -   `cluster` (INTEGER): The cluster ID assigned to the article by K-Means.
    -   `headline` (TEXT): The main headline of the article.
    -   `content` (TEXT): The primary content/lead paragraph of the article.
    -   `compound` (NUMERIC): Compound sentiment score (VADER).
    -   `neg` (NUMERIC): Negative sentiment score (VADER).
    -   `neu` (NUMERIC): Neutral sentiment score (VADER).
    -   `pos` (NUMERIC): Positive sentiment score (VADER).
-   **`ml_models`**: Table for storing serialized (persisted) machine learning models.
    -   `id` (SERIAL PRIMARY KEY): Unique identifier for the stored model.
    -   `model_name` (TEXT): Name of the model (e.g., 'tfidf_vectorizer', 'kmeans_model').
    -   `model_data` (BYTEA): Binary representation of the serialized model data.
    -   `created_at` (TIMESTAMP): Timestamp when the model was stored.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE.md) (please ensure you have a `LICENSE.md` file in your repository if you intend to use this).

---

## 👋 Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.
