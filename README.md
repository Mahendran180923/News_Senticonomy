# 📊 Senticonomy: News Sentiment Analysis and Economic Impact Visualization

Senticonomy is a web-based application that collects and analyzes historical and real-time news data to compute sentiment scores across various categories like business, politics, technology, and more. It provides meaningful visual insights on how public sentiment may influence economic trends.

---

## 🚀 Key Features

- 🔍 **News Aggregation** Kaggle Dataset
- 🧹 **Data Cleaning & Preprocessing** using NLP libraries (NLTK, Pandas)
- 🧠 **Clustering Algorithms** to group related news content
- ❤️ **Sentiment Analysis** using VADER, TextBlob, and BERT-based models
- 📊 **Data Visualization** with Plotly, Matplotlib
- ☁️ **AWS Integration** with S3 and RDS for scalable data storage
- 🌐 **Interactive Web App** dashboard for sentiment insights


## 🧠 Skills You’ll Learn
- Utilizing **NLP techniques** for text cleaning, sentiment, and clustering
- Building **interactive dashboards** and analytics tools
- Using **AWS (S3, EC2, RDS)** for cloud data storage and deployment

---

## 🧰 Tech Stack

| Technology        | Description                            |
|-------------------|----------------------------------------|
| Python            | Core scripting and data processing     |
| AWS S3, RDS       | Cloud-based data storage and management|
| NLP Libraries     | NLTK          |
| Visualization     | Plotly, Matplotlib               |
| Clustering        | KMeans                    |
| Web Framework     | Streamlit             |
| Version Control   | GitHub                           |

---

## 🧾 Dataset Overview

- **Sources**: Kaggle
- **Formats**: CSV
- **Fields**:
  - `Headline`
  - `Content`
  - `Date`
  - `Source`
  - `Category`
  - `Sentiment Score`

### Data Preprocessing Includes:
- Tokenization  
- Stopword removal  
- Text normalization  
- Sentiment score assignment using NLP models  



Set up a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:
pip install -r requirements.txt


Run the app:
data_visualisation.py


