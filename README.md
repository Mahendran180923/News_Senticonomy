# 📰 News Sentiment Analysis & Clustering Dashboard

![News Sentiment Dashboard](https://user-images.githubusercontent.com/123456789/your-dashboard-image.png)

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
  - Filtered data table
  - 📊 Sentiment trends, distribution, and volume trends
  - 🔥 Sentiment extremes (min/max)
  - ☁️ Word clouds (overall, by cluster, by sentiment)
  - 🧊 Category-cluster comparisons & heatmaps
  - 🏆 Top N articles by sentiment
  - 🎨 Customizable dashboard theme

---

## 📁 Project Structure

```
data_collection.py      # Download and filter raw data from Kaggle
aws_upload.py           # Uploads raw_data.csv to AWS S3
aws.download.py         # Downloads raw_data.csv from S3
data_cleaning.py        # Cleans and enriches news data for modeling
model.py                # Preprocessing, clustering, sentiment analysis, DB storage
data_visualisation.py   # Streamlit dashboard visualization
.vscode/secrets.json    # (Not provided) AWS credentials
README.md               # This file
```

---

## 🗂️ Data Source

- Uses "NYT Articles (21M+, 2000-Present)" dataset from Kaggle  
  [Get it here](https://www.kaggle.com/datasets/aryansingh0909/nyt-articles-21m-2000-present)  
  ```bash
  kaggle datasets download -d aryansingh0909/nyt-articles-21m-2000-present
  ```

---

## 🛠️ Prerequisites

- 🐍 **Python 3.8+**
- 🐘 **PostgreSQL Database**
- ☁️ **AWS Account** (optional, for S3)
- 🔑 **Kaggle API Key** (optional for CLI download)

---

## ⚙️ Installation

1. **Clone the repo:**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

3. **Install dependencies:**  
   Create `requirements.txt` with:
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
    Then:
    ```bash
    pip install -r requirements.txt
    ```

4. **NLTK Data:**  
   `model.py` auto-downloads needed NLTK resources.

---

## 🔐 Configuration

1. **AWS Credentials (`.vscode/secrets.json`):**
    ```json
    {
      "AWS_ACCESS_KEY": "YOUR_AWS_ACCESS_KEY",
      "AWS_SECRET_KEY": "YOUR_AWS_SECRET_KEY"
    }
    ```
    > ⚠️ *Do NOT commit this file to public repos!*

2. **PostgreSQL Credentials:**  
   Set these environment variables:
    ```bash
    export DB_HOST="your_db_host"
    export DB_NAME="your_database_name"
    export DB_USER="your_username"
    export DB_PASSWORD="your_password"
    export DB_PORT="5432"
    ```

---

## ▶️ Usage

1. **Data Collection:**  
    Download, unzip, and run:
    ```bash
    python data_collection.py
    ```
2. **AWS S3 (Optional):**
    - **Upload:** `python aws_upload.py`
    - **Download:** `python aws.download.py`
3. **Data Cleaning:**  
    ```bash
    python data_cleaning.py
    ```
4. **Model Training & Processing:**  
    ```bash
    python model.py
    ```
5. **Run the Dashboard!**  
    ```bash
    streamlit run data_visualisation.py
    ```
    ![Streamlit Screenshot](https://user-images.githubusercontent.com/123456789/your-screenshot-image.png)

---

## 🗄️ Database Schema

- **news_data_processed**: Cleaned and enriched news articles  
  - `date`, `category`, `cluster`, `headline`, `content`, `compound`, `neg`, `neu`, `pos`
- **ml_models**: Serialized ML models  
  - `id`, `model_name`, `model_data (BYTEA)`, `created_at`

---

## 📃 License

Open-source under the [MIT License](LICENSE.md)  
✨ Contributions welcome! Open an issue or submit a PR.

---

## 🙌 Contributing

Pull requests and suggestions are encouraged!  
Feel free to open issues or submit improvements.

---

> Made with ❤️ for data, news, and insights!
