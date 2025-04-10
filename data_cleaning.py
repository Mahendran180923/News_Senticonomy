import pandas as pd
import ast
import numpy as np
import os


# Read csv file and store as Dataframe
uncleaned_data = pd.read_csv('uncleaned_data.csv')
df = pd.DataFrame(uncleaned_data)


pd.set_option('display.max_colwidth', None)

# print(df.head())
# print(df.info())


# Drop the column name "Unnamed"
df.drop(['Unnamed: 0'], axis=1, inplace=True)


# convert the date into datetime format
df['pub_date'] = pd.to_datetime(df['pub_date'])


# Extract day, month, year and time from 'pub_date' column for better analysis

df['year'] = df['pub_date'].dt.year
df['month'] = df['pub_date'].dt.month
df['day'] = df['pub_date'].dt.day
df['day_of_week'] = df['pub_date'].dt.day_name()
df['date'] = df['pub_date'].dt.date
df['time'] = df['pub_date'].dt.time




# Extract main Headline from headline column which has dictionary type of data
df['headline'] = df['headline'].apply(lambda x: ast.literal_eval(x)['main'])



# Fill the lead_paragraph column with abstract column info where lead_paragraph column has only the info of "To the Editor:" (Seen in many rows)
df['lead_paragraph'] = np.where(df['lead_paragraph'] == 'To the Editor:',
                                   df['abstract'] ,
                                   df['lead_paragraph'])


# Rename the column names for better understanding
df.rename(columns={'lead_paragraph': 'content', 'section_name': 'category'}, inplace=True)


# Filtering the news category
# unique_categories, counts = np.unique(df['category'], return_counts=True)
# for category, count in zip(unique_categories, counts):
#     print(f"{category}: {count}")


category = ["Travel", "Technology", "Science", "Health", "Food", "Education", "Sports"]
df = df[df['category'].isin(category)]


unique_categories, counts = np.unique(df['category'], return_counts=True)

for category, count in zip(unique_categories, counts):
    print(f"{category}: {count}")

df.drop(['abstract', 'pub_date'], axis=1, inplace=True)

print(df.isnull().sum())

new_df = df[['date', 'time', 'headline', 'content', 'web_url', 'category', 'day', 'month', 'day_of_week', 'year']]

new_df.to_csv('cleaned_news_data.csv')


file_size = os.path.getsize('cleaned_news_data.csv')

if file_size < 1024:
    print(f"The size of the CSV file is: {file_size} bytes")
elif file_size < 1024 ** 2:
    print(f"The size of the CSV file is: {file_size / 1024:.2f} KB")
else:
    print(f"The size of the CSV file is: {file_size / (1024 ** 2):.2f} MB")
