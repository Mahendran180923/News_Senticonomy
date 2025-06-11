import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd



st.config.set_option('theme.base', 'light')
st.config.set_option('theme.primaryColor', '#907474')
st.config.set_option('theme.backgroundColor', '#F9EBE7')
st.config.set_option('theme.secondaryBackgroundColor', '#F9F3F1')
st.config.set_option('theme.textColor', '#020412')
st.set_page_config(layout='wide')

# # Create a copy of the DataFrame
df = pd.read_csv("final_data.csv")


# Create a sidebar
st.sidebar.title("News Sentiment Analysis")

# Add options to the sidebar
word_cloud = st.sidebar.checkbox("Word Cloud")
sentiment_trend = st.sidebar.checkbox("Sentiment Trend by Category")
year_month_trend = st.sidebar.checkbox("Year/Month_wise Trend")
year_quarter_trend = st.sidebar.checkbox("Year/Quarter_wise Trend")
bar_line_chart = st.sidebar.checkbox("Bar and Line Chart by Date Range")
table = st.sidebar.checkbox("Table by Date Range")
category_month_year_comparison = st.sidebar.checkbox("Category-wise Month and Year Comparison")
category_sentiment_bar_chart = st.sidebar.checkbox("Category-wise Sentiment Bar Chart")
sentiment_word_cloud = st.sidebar.checkbox("Sentiment Word Cloud")



# Function to create word cloud
def create_word_cloud(cluster):
    cluster_text = " ".join(df[df['cluster'] == cluster]['headline'].astype(str).fillna(''))
    wordcloud = WordCloud(background_color='white').generate(cluster_text)
    return wordcloud


if word_cloud:
    clusters = sorted(df['cluster'].unique())
    n_clusters = len(clusters)
    n_cols = 3
    n_rows = (n_clusters + n_cols - 1) // n_cols  # Calculate the number of rows needed
    fig, axs = plt.subplots(n_rows, n_cols, figsize=(15, n_rows * 5))
    for i, cluster in enumerate(clusters):
        row = i // n_cols
        col = i % n_cols
        axs[row, col].imshow(create_word_cloud(cluster), interpolation='bilinear')
        axs[row, col].axis('off')
        axs[row, col].set_title(f"Cluster {cluster}")
    # Hide any unused subplots
    for i in range(n_clusters, n_rows * n_cols):
        row = i // n_cols
        col = i % n_cols
        axs[row, col].axis('off')
    plt.tight_layout()
    st.pyplot(fig)


if sentiment_trend:
    # Function to create sentiment trend plot
    def create_sentiment_trend_plot():
        sentiment_trend = df.groupby(['year', 'category'])['compound'].mean().reset_index()
        fig = px.line(sentiment_trend, x='year', y='compound', color='category', title='Sentiment Trend Over Time', markers=True, labels={"compound": "Average Sentiment Score", "category": "News Category"})
        return fig
    st.write("Sentiment Trend Plot")
    st.plotly_chart(create_sentiment_trend_plot())


if year_month_trend:
    # Function to create line chart
    def month_wise_trend():
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        
        years = df['year'].unique()
        selected_years = st.multiselect("Select Years", years)
        
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        selected_months = st.multiselect("Select Months", months)
        
        fig = go.Figure()
        
        month_map = {month: i+1 for i, month in enumerate(months)}
        
        for year in selected_years:
            for month in selected_months:
                month_num = month_map[month]
                filtered_df = df[(df['year'] == year) & (df['month'] == month_num)]
                avg_compound = filtered_df.groupby(['category'])['compound'].mean().reset_index()
                fig.add_trace(go.Scatter(x=avg_compound['category'], y=avg_compound['compound'], mode='lines', name=f"{year} - {month}"))
        
        fig.update_layout(title="Year/Month_wise Trend", xaxis_title="Category", yaxis_title="Compound")
        
        return fig
    st.write("Year/Month_wise Trend")
    st.plotly_chart(month_wise_trend())


if year_quarter_trend:
    # Function to create line chart
    def quarter_wise_trend():
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        df['quarter'] = df['date'].dt.quarter
        
        years = df['year'].unique()
        selected_years = st.multiselect("Select Years", years)
        
        quarters = ['Q1', 'Q2', 'Q3', 'Q4']
        selected_quarters = st.multiselect("Select Quarters", quarters)
        
        fig = go.Figure()
        
        for year in selected_years:
            for quarter in selected_quarters:
                quarter_num = int(quarter.split('Q')[1])
                filtered_df = df[(df['year'] == year) & (df['quarter'] == quarter_num)]
                avg_compound = filtered_df.groupby(['category'])['compound'].mean().reset_index()
                fig.add_trace(go.Scatter(x=avg_compound['category'], y=avg_compound['compound'], mode='lines', name=f"{year} - {quarter}"))
        
        fig.update_layout(title="Year/Quarter_wise Trend", xaxis_title="Category", yaxis_title="Compound")
        
        return fig
    st.write("Year/Quarter_wise Trend")
    st.plotly_chart(quarter_wise_trend())

if bar_line_chart:
    # Function to create bar and line chart by date range
    def create_bar_and_line_chart_by_date_range():
        df['date'] = pd.to_datetime(df['date'])
        min_date = df['date'].min()
        max_date = df['date'].max()
        
        start_date = st.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
        end_date = st.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)
        
        filtered_df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]
        
        avg_compound = filtered_df.groupby(['category'])['compound'].mean().reset_index()
        
        fig = go.Figure(data=[go.Bar(x=avg_compound['category'], y=avg_compound['compound'], name='Bar Chart'), 
                           go.Scatter(x=avg_compound['category'], y=avg_compound['compound'], mode='lines', name='Line Chart')])

        fig.update_layout(title=f"Bar and Line Chart from {start_date} to {end_date}")
        
        return fig
    st.write("Bar and Line Chart by Date Range")
    st.plotly_chart(create_bar_and_line_chart_by_date_range())


if table:
    # Function to table by date range
    def create_table_by_date_range():
        df['date'] = pd.to_datetime(df['date'])
        df.drop(['Unnamed: 0',  'day_of_week', 'year', 'content', 'neg', 'neu', 'pos'], axis=1, inplace=True)
        min_date = df['date'].min()
        max_date = df['date'].max()
        start_date = st.date_input("Start Date", min_value=min_date, max_value=max_date, value=None)
        end_date = st.date_input("End Date", min_value=min_date, max_value=max_date, value=None)
        filtered_df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]
        return filtered_df

    st.write("Table by Date Range")
    st.table(create_table_by_date_range())







if category_month_year_comparison:
    # Function to create category-wise month and year comparison chart
    def create_category_wise_month_and_year_comparison_chart():
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.month
        df['year'] = df['date'].dt.year
        
        categories = df['category'].unique()
        selected_categories = st.multiselect("Select Categories", categories)
        
        years = df['year'].unique()
        selected_years = st.multiselect("Select Years", ['All Years'] + list(years))
        
        month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 
                       7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
        
        fig = go.Figure()
        
        if 'All Years' in selected_years:
            selected_years = list(years)
        
        for category in selected_categories:
            for year in selected_years:
                filtered_df = df[(df['category'] == category) & (df['year'] == year)]
                avg_compound = filtered_df.groupby(['month'])['compound'].mean().reset_index()
                fig.add_trace(go.Scatter(x=[month_names[m] for m in avg_compound['month']], y=avg_compound['compound'], mode='lines', name=f"{category} - {year}"))
        
        fig.update_layout(title="Category-wise Month Comparison", xaxis_title="Month", yaxis_title="Compound")
        
        return fig
    st.write("Category-wise Month and Year Comparison")
    st.plotly_chart(create_category_wise_month_and_year_comparison_chart())


if category_sentiment_bar_chart:
    # Function to create category-wise sentiment bar chart
    def create_category_wise_sentiment_bar_chart():
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        
        categories = df['category'].unique()
        years = df['year'].unique()
        
        selected_years = st.multiselect("Select Years", years)
        
        fig = go.Figure()
        
        for year in selected_years:
            category_values = []
            for category in categories:
                filtered_df = df[(df['category'] == category) & (df['year'] == year)]
                if not filtered_df.empty:
                    category_values.append(filtered_df['compound'].mean().round(2))
                else:
                    category_values.append(0)
            fig.add_trace(go.Bar(x=categories, y=category_values, name=year))
        
        fig.update_layout(title="Category-wise Sentiment Bar Chart", xaxis_title="Category", yaxis_title="Average Sentiment Score", barmode='group')
        
        return fig
    st.write("Category-wise Sentiment Bar Chart")
    st.plotly_chart(create_category_wise_sentiment_bar_chart())



if sentiment_word_cloud:
    # Function to create sentiment word cloud
    def create_sentiment_word_cloud():
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        
        years = df['year'].unique()
        selected_year = st.selectbox("Select Year", years)
        
        filtered_df = df[(df['year'] == selected_year)]
        
        positive_words = filtered_df[filtered_df['compound'] > 0.5]['content']
        negative_words = filtered_df[filtered_df['compound'] < -0.5]['content']
        neutral_words = filtered_df[(filtered_df['compound'] >= -0.5) & (filtered_df['compound'] <= 0.5)]['content']
        
        positive_wordcloud = WordCloud(width=800, height=400, max_words=100, background_color='white').generate(' '.join(positive_words.astype(str)))
        negative_wordcloud = WordCloud(width=800, height=400, max_words=100, background_color='white').generate(' '.join(negative_words.astype(str)))
        neutral_wordcloud = WordCloud(width=800, height=400, max_words=100, background_color='white').generate(' '.join(neutral_words.astype(str)))
        
        fig, ax = plt.subplots(1, 3, figsize=(20, 10))
        ax[0].imshow(positive_wordcloud, interpolation='bilinear')
        ax[0].set_title('Positive Sentiment')
        ax[0].axis('off')
        ax[1].imshow(negative_wordcloud, interpolation='bilinear')
        ax[1].set_title('Negative Sentiment')
        ax[1].axis('off')
        ax[2].imshow(neutral_wordcloud, interpolation='bilinear')
        ax[2].set_title('Neutral Sentiment')
        ax[2].axis('off')
        
        st.pyplot(fig)
    st.write("Sentiment Word Cloud")
    create_sentiment_word_cloud()
