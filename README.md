# News Sentiment Analysis and Clustering Dashboard

## Project Overview

This project provides a comprehensive solution for analyzing news article sentiment and identifying intrinsic clusters within the articles. It encompasses a full data pipeline from collection and cleaning to machine learning model application (K-Means clustering and VADER sentiment analysis) and finally, an interactive Streamlit dashboard for visualization. Data persistence is managed using PostgreSQL, and raw data can optionally be stored in AWS S3.

## Features

* **Automated Data Collection:** Downloads and processes a large news article dataset from Kaggle.
* **Robust Data Cleaning:** Handles missing values, extracts relevant information (date components, main headlines), and filters data by categories and date ranges.
* **Text Preprocessing:** Utilizes NLTK for tokenization, lemmatization, and stop word removal for effective text analysis.
* **Feature Extraction:** Employs TF-IDF (Term Frequency-Inverse Document Frequency) to convert text data into numerical vectors suitable for machine learning.
* **K-Means Clustering:** Groups similar news articles into distinct clusters based on their content. The number of clusters is dynamically determined by the unique categories in the data.
* **VADER Sentiment Analysis:** Calculates polarity scores (negative, neutral, positive, and compound) for news article content to determine the overall sentiment.
* **PostgreSQL Integration:** Stores processed news data and the trained K-Means model in a PostgreSQL database, ensuring data persistence and easy retrieval for the dashboard.
* **AWS S3 Integration (Optional):** Provides scripts to upload and download raw data to and from an S3 bucket for cloud storage and backup.
* **Interactive Streamlit Dashboard:** A user-friendly web interface allowing users to:
    * Apply global filters (date range, categories, clusters).
    * View a **Filtered Data Table** of processed articles.
    * Visualize **Sentiment Trends** over time (overall, year/month, year/quarter).
    * Analyze **Sentiment Distribution** by category or cluster.
    * Explore **News Volume Trends** (daily/weekly).
    * Identify **Sentiment Extremes** (min/max daily sentiment).
    * Generate **Word Clouds** for overall content, by cluster, and by sentiment (positive, negative, neutral).
    * Examine **Category-Cluster Comparison Tables** and **Heatmaps** to understand content distribution.
    * Discover **Top N Articles** by sentiment (most positive/negative).
    * Customizable dashboard theme colors for a modern look.

## Project Structure

* `data_collection.py`: Downloads the raw news dataset, filters it by date, performs initial column drops, and saves it as `raw_data.csv`.
* `aws_upload.py`: Uploads `raw_data.csv` to an AWS S3 bucket.
* `aws.download.py`: Downloads `raw_data.csv` from the AWS S3 bucket and saves it as `downloaded_data.csv`.
* `data_cleaning.py`: Reads `downloaded_data.csv`, performs extensive cleaning, extracts features like date components, processes headlines, renames columns, filters specific categories, and saves the cleaned data as `cleaned_news_data.csv`.
* `model.py`: Orchestrates the machine learning pipeline. It performs text preprocessing, TF-IDF vectorization, K-Means clustering, VADER sentiment analysis, stores the trained K-Means model, and pushes the final processed data to PostgreSQL.
* `data_visualisation.py`: The Streamlit application for the interactive dashboard. It fetches processed data from PostgreSQL and presents various visualizations based on user-selected filters.
* `.vscode/secrets.json`: (Not provided, but implied by `aws_upload.py` and `aws.download.py`) Stores sensitive AWS credentials.
* `README.md`: This file.

## Data Source

The project utilizes the "NYT Articles (21M+, 2000-Present)" dataset available on Kaggle.
To download, use the Kaggle CLI command:
`kaggle datasets download -d aryansingh0909/nyt-articles-21m-2000-present`

## Prerequisites

Before running the project, ensure you have the following installed:

* **Python 3.8+**
* **PostgreSQL Database:** A running PostgreSQL instance is required to store the processed data and the ML model.
* **AWS Account (Optional but Recommended):** For utilizing S3 for raw data storage.
* **Kaggle API Key:** To download the dataset programmatically if you prefer not to download it manually.

## Installation

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
    Create a `requirements.txt` file with the following packages:
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
    joblib # Although pickle is used, joblib is imported. Include if you plan to use it.
    ```
    Then install them:
    ```bash
    pip install -r requirements.txt
    ```

4.  **NLTK Data Downloads:**
    The `model.py` script automatically checks and downloads necessary NLTK data (`punkt`, `wordnet`, `stopwords`, `vader_lexicon`) when run.

## Configuration

1.  **AWS Credentials (`.vscode/secrets.json`):**
    If you plan to use AWS S3 for data storage, create a `.vscode` directory in your project root and inside it, create a `secrets.json` file with your AWS Access Key and Secret Key:
    ```json
    {
        "AWS_ACCESS_KEY": "YOUR_AWS_ACCESS_KEY",
        "AWS_SECRET_KEY": "YOUR_AWS_SECRET_KEY"
    }
    ```
    **Security Note:** Do not commit this file to public repositories. Consider using environment variables or AWS Secrets Manager for production environments.

2.  **PostgreSQL Database Credentials:**
    The Python scripts use environment variables for PostgreSQL connection details. Set the following environment variables:
    ```bash
    export DB_HOST="your_db_host" # e.g., localhost
    export DB_NAME="your_database_name" # e.g., mdte16db
    export DB_USER="your_username" # e.g., postgres
    export DB_PASSWORD="your_password"
    export DB_PORT="5432" # Default PostgreSQL port
    ```
    Ensure your PostgreSQL database `mdte16db` (or your chosen name) exists and your user has the necessary permissions.

## Usage

Follow these steps to run the complete data pipeline and launch the dashboard:

1.  **Data Collection:**
    Download the dataset from Kaggle manually or using the Kaggle CLI, and place `nyt-articles-21m-2000-present.zip` in the project root. Then run:
    ```bash
    python data_collection.py
    ```
    This will extract `nyt-metadata.csv` and generate `raw_data.csv`.

2.  **AWS S3 Operations (Optional):**
    * **Upload `raw_data.csv` to S3:**
        ```bash
        python aws_upload.py
        ```
    * **Download `raw_data.csv` from S3:** (If you prefer to download from S3 instead of using the local `raw_data.csv` directly for cleaning)
        ```bash
        python aws.download.py
        ```
        This will create `downloaded_data.csv`.

3.  **Data Cleaning:**
    This script processes `downloaded_data.csv` (or `raw_data.csv` if `aws.download.py` was skipped) to create a clean dataset.
    ```bash
    python data_cleaning.py
    ```
    This will generate `cleaned_news_data.csv`.

4.  **Model Training and Data Processing:**
    This script performs text preprocessing, clustering, sentiment analysis, stores the trained model in the database, and pushes the final processed data to the PostgreSQL table `news_data_processed`.
    ```bash
    python model.py
    ```

5.  **Launch the Streamlit Dashboard:**
    ```bash
    streamlit run data_visualisation.py
    ```
    This will open the interactive dashboard in your web browser.

## Database Schema

The `model.py` script creates two tables in your PostgreSQL database:

1.  `news_data_processed`:
    * Stores the cleaned and enriched news article data.
    * Key columns include: `date`, `category`, `cluster`, `headline`, `content`, `compound`, `neg`, `neu`, `pos`.

2.  `ml_models`:
    * Stores serialized machine learning models (currently, the K-Means model).
    * Columns: `id`, `model_name`, `model_data` (BYTEA for binary model data), `created_at`.

## License

This project is open-source and available under the [MIT License](LICENSE.md) (or specify your chosen license).

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.
