# 📰 News Sentiment Analysis & Clustering Dashboard

![Overall Dashboard View with Filters](images/Screenshot%202025-06-24%20014019.png)

## 🚀 Project Overview

This project delivers a complete pipeline for analyzing news article sentiment and discovering clusters within the articles. From automated data collection and cleaning 🧹 to interactive visualization 📊, it’s your one-stop solution for news insights.

---

## ✨ Features

- 🤖 **Automated Data Collection:** Downloads and processes a large news article dataset from Kaggle.
- 🧼 **Robust Data Cleaning:** Handles missing values, extracts dates/headlines, filters by category and date.
- 📝 **Text Preprocessing:** Uses NLTK for tokenization, lemmatization, and stopword removal.
- 📈 **Feature Extraction:** Converts text to numerical vectors using TF-IDF for machine learning.
- 🔎 **K-Means Clustering:** Groups similar articles into clusters based on content.
- 😄 **VADER Sentiment Analysis:** Calculates polarity scores (negative/neutral/positive/compound).
- 🗃️ **PostgreSQL Integration:** Stores processed data & model for persistent and efficient dashboard access.
- ☁️ **AWS S3 Integration (Optional):** Upload/download raw data to/from an S3 bucket.
- 🌐 **Interactive Streamlit Dashboard:**
  - Apply global filters (date, category, cluster)

  - **Filtered Data Table:** View a summary of articles based on your global filter selections.
    ![Interactive Filtered Data Table](images/Screenshot%202025-06-24%20013734.png)

  - **Sentiment Trends & Distribution:**
    - **Overall Sentiment Trend by Category:** Track the average sentiment score for each news category over time.
      ![Overall Sentiment Trend by Category](images/Screenshot%202025-06-24%20013852.png)
    - **Sentiment Trend (Year/Month-wise):** Compare category sentiment across selected years and months.
      ![Sentiment Trend (Year/Month-wise)](images/Screenshot%202025-06-24%20013839.png)
    - **Sentiment Trend (Year/Quarter-wise):** Compare category sentiment across selected years and quarters.
      ![Sentiment Trend (Year/Quarter-wise)](images/Screenshot%202025-06-24%20014056.png)
    - **Category-wise Sentiment Bar Chart:** Visualize the average sentiment score for each category across selected years.
      ![Category-wise Sentiment Bar Chart](images/Screenshot%202025-06-24%20013805.png)
    - **Category Sentiment (Month/Year Comparison):** Compare sentiment trends for specific categories across different months and years.
      ![Category Sentiment (Month/Year Comparison)](images/Screenshot%202025-06-24%20014117.png)
    - **Sentiment Score Distribution:** Explore the distribution of sentiment scores by category or cluster.
      ![Sentiment Score Distribution](images/Screenshot%202025-06-24%20013959.png)
    - **News Volume Trend:** Analyze the daily or weekly volume of news articles.
      ![Daily/Weekly News Volume Trend](images/Screenshot%202025-06-24%20013824.png)
    - **Sentiment Extremes (Min/Max):** Track the minimum (most negative) and maximum (most positive) sentiment scores over time.

  - **Word Clouds:**
    - **Word Cloud by Cluster:** Visualize the most frequent words in headlines for each identified cluster.
      ![Word Cloud by Cluster](images/Screenshot%202025-06-24%20013909.png)
    - **Sentiment Word Cloud (Positive/Negative/Neutral):** Explore words associated with positive, negative, and neutral sentiments for a selected year.
      ![Sentiment Word Cloud](images/Screenshot%202025-06-24%20014040.png)

  - **Category-Cluster Comparison:**
    - **Heatmap of Category vs. Cluster Counts:** A dense overview of the counts for each Category-Cluster pair.
      ![Heatmap of Category vs. Cluster Counts](images/Screenshot%202025-06-24%20013925.png)
    - Category-Cluster Comparison Tables.

  - **Top N Articles by Sentiment:** View the most positive or most negative articles based on current filters.
    ![Top N Articles by Sentiment](images/Screenshot%202025-06-24%20013940.png)

---

## 🗄️ Data Source

The project utilizes the "NYT Articles (21M+, 2000-Present)" dataset available on Kaggle.
To download, use the Kaggle CLI command: `kaggle datasets download -d aryansingh0909/nyt-articles-21m-2000-present`

## ⚙️ Prerequisites

Before running the project, ensure you have the following installed:

* **Python 3.8+**
* **PostgreSQL Database:** A running PostgreSQL instance is required to store the processed data and the ML model.
* **AWS Account (Optional but Recommended):** For utilizing S3 for raw data storage.
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

## ▶️ Usage

1.  **Data Collection:**
    Download the dataset from Kaggle manually or using the Kaggle CLI, and place `nyt-articles-21m-2000-present.zip` in the project root. Then run:
    ```bash
    python data_collection.py
    ```

2.  **AWS S3 (Optional):**
    * **Upload `raw_data.csv` to S3:**
        ```bash
        python aws_upload.py
        ```
    * **Download `raw_data.csv` from S3:** (If you prefer to download from S3 instead of using the local `raw_data.csv` directly for cleaning)
        ```bash
        python aws.download.py
        ```

3.  **Data Cleaning:**
    This script processes `downloaded_data.csv` (or `raw_data.csv` if `aws.download.py` was skipped) to create a clean dataset.
    ```bash
    python data_cleaning.py
    ```

4.  **Model Training & Processing:**
    This script performs text preprocessing, clustering, sentiment analysis, stores the trained model in the database, and pushes the final processed data to the PostgreSQL table `news_data_processed`.
    ```bash
    python model.py
    ```

5.  **Run the Dashboard!**
    ```bash
    streamlit run data_visualisation.py
    ```

---

## 🗄️ Database Schema

-   **`news_data_processed`**: Cleaned and enriched news articles
    -   `date`, `category`, `cluster`, `headline`, `content`, `compound`, `neg`, `neu`, `pos`
-   **`ml_models`**: Serialized ML models
    -   `id`, `model_name`, `model_data` (BYTEA for binary model data), `created_at`

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE.md) (please ensure you have a `LICENSE.md` file in your repository if you intend to use this).

---

## 👋 Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.
