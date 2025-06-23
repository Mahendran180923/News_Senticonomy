import zipfile
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz



# Data source - Collected from Kaggle Dataset
# https://www.kaggle.com/datasets/aryansingh0909/nyt-articles-21m-2000-present
# kaggle datasets download -d aryansingh0909/nyt-articles-21m-2000-present



# Unzip the downloaded file
with zipfile.ZipFile('nyt-articles-21m-2000-present.zip', 'r') as zip_ref:
    zip_ref.extractall()

#Read CSV file using pandas library
data = pd.read_csv('nyt-metadata.csv')
# print(data.info())

# Copy the data in different variable for future reference
df = pd.DataFrame(data)

# Drop unwatned columns

df.drop(['print_section', 
         'snippet', 'print_page', 
         'document_type', 'byline', 'keywords',  
         'news_desk', 'type_of_material',  '_id', 
         'word_count', 'uri', 'multimedia', 
         'subsection_name'], axis=1, inplace=True)

# df.isnull().sum()

# drop the row where date is having null values
df.dropna(subset=['pub_date'], inplace=True)


# Fill the null values in the leadparagraph column from abstract 
df['lead_paragraph'] = np.where(df['lead_paragraph'].isnull(),
                                   df['abstract'],
                                   df['lead_paragraph'])

# Drop rows if its having a null values
df.dropna(how='any', inplace=True)
# df.isnull().sum()


# Convert the date into datetime format from object
df['pub_date'] = pd.to_datetime(df['pub_date'])

# Create start and end date range for data filtering
start_date = datetime(2015,1,1, tzinfo=pytz.UTC)

end_date = datetime(2025,6,21, tzinfo=pytz.UTC)


# Filter the DataFrame to include only rows with pub_date within the last 10 years
df_filtered = df[(df['pub_date'] >= start_date) & (df['pub_date'] <= end_date)]

# Print the first few rows of the filtered DataFrame
print(df_filtered.head())
print(df_filtered.isnull().sum())

# Store the dataframe as CSV file
df_filtered.to_csv('raw_data.csv')
