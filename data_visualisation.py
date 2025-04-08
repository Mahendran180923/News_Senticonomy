import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd




st.config.set_option('theme.base', 'light')
st.config.set_option('theme.primaryColor', '#907474')
st.config.set_option('theme.backgroundColor', '#C1A3A3')
st.config.set_option('theme.secondaryBackgroundColor', '#B93413')
st.config.set_option('theme.textColor', '#020412')
st.set_page_config(layout='wide')

# # Create a copy of the DataFrame
df = pd.read_csv("final_data.csv")


st.title("News Sentiment Analysis")
selected_option = st.radio(
    "Select an option:",
    ("Word Cloud", "Sentiment Trend Plot", "Sentiment Trend Plot with Dropdown", "Bar and Line Chart")
)

# Function to create word cloud
def create_word_cloud(cluster):
    cluster_text = " ".join(df[df['cluster'] == cluster]['headline'].astype(str).fillna(''))
    wordcloud = WordCloud(background_color='white').generate(cluster_text)
    return wordcloud

if selected_option == "Word Cloud":
    clusters = df['cluster'].unique()
    for i, cluster in enumerate(clusters):
        st.write(f"Word Cloud for Cluster {cluster}")
        fig, ax = plt.subplots()
        ax.imshow(create_word_cloud(cluster), interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

elif selected_option == "Sentiment Trend Plot":
    # Function to create sentiment trend plot
    def create_sentiment_trend_plot():
        sentiment_trend = df.groupby(['year', 'category'])['compound'].mean().reset_index()
        fig = px.line(sentiment_trend, x='year', y='compound', color='category', title='Sentiment Trend Over Time', markers=True, labels={"compound": "Average Sentiment Score", "category": "News Category"})
        return fig
    st.write("Sentiment Trend Plot")
    st.plotly_chart(create_sentiment_trend_plot())


elif selected_option == "Sentiment Trend Plot with Dropdown":
    # Function to create sentiment trend plot with dropdown
    def create_sentiment_trend_plot_with_dropdown():
        sentiment_trend = df.groupby(['year', 'category'])['compound'].mean().reset_index()
        years = sorted(sentiment_trend['year'].unique())
        fig = px.line(sentiment_trend[sentiment_trend['year'] == years[0]], x='category', y='compound', color='category', title=f'Sentiment Trend in {years[0]}', markers=True, labels={"compound": "Average Sentiment Score", "category": "News Category"})
        dropdown_button = [dict(label=str(y), method='update', args=[{ "x": [sentiment_trend[sentiment_trend['year'] == y]['category']], "y": [sentiment_trend[sentiment_trend['year'] == y]['compound']], "type": "scatter" }, {"title": f"Sentiment score by category for {y}"} ]) for y in years]
        fig.update_layout(updatemenus=[dict(type='dropdown', buttons=dropdown_button, direction='down', showactive=True, x=0.1, xanchor='left', y=1.15, yanchor='top')])
        return fig
    st.write("Sentiment Trend Plot with Dropdown")
    st.plotly_chart(create_sentiment_trend_plot_with_dropdown())

elif selected_option == "Bar and Line Chart":
    # Function to create bar and line chart
    def create_bar_and_line_chart():
        df['date'] = pd.to_datetime(df['pub_date'])
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        avg_compound = df.groupby(['year', 'month', 'category'])['compound'].mean().reset_index()
        years = sorted(df['year'].unique())
        months = sorted(df['month'].unique())
        
        # Create a dictionary to map month numbers to month names
        month_names = {
            1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
            7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
        }
        
        fig = go.Figure(data=[go.Bar(x=avg_compound[(avg_compound['year'] == years[0]) & (avg_compound['month'] == months[0])]['category'], y=avg_compound[(avg_compound['year'] == years[0]) & (avg_compound['month'] == months[0])]['compound'], name='Bar Chart'), 
                             go.Scatter(x=avg_compound[(avg_compound['year'] == years[0]) & (avg_compound['month'] == months[0])]['category'], y=avg_compound[(avg_compound['year'] == years[0]) & (avg_compound['month'] == months[0])]['compound'], mode='lines', name='Line Chart')])
        
        year_buttons = []
        for y in years:
            filtered_data = avg_compound[(avg_compound['year'] == y) & (avg_compound['month'] == months[0])]
            year_buttons.append(dict(label=str(y), method='update', args=[{ "x": [filtered_data['category'], filtered_data['category']], "y": [filtered_data['compound'], filtered_data['compound']] }]))
        
        month_buttons = []
        for m in months:
            filtered_data = avg_compound[(avg_compound['year'] == years[0]) & (avg_compound['month'] == m)]
            month_buttons.append(dict(label=month_names[m], method='update', args=[{ "x": [filtered_data['category'], filtered_data['category']], "y": [filtered_data['compound'], filtered_data['compound']] }]))
        
        fig.update_layout(
            updatemenus=[
                dict(
                    type='dropdown',
                    buttons=year_buttons,
                    direction='down',
                    showactive=True,
                    x=0.1,
                    xanchor='left',
                    y=1.15,
                    yanchor='top',
                    pad={"r": 10, "t": 10},
                    name="Year"
                ),
                dict(
                    type='dropdown',
                    buttons=month_buttons,
                    direction='down',
                    showactive=True,
                    x=0.4,
                    xanchor='left',
                    y=1.15,
                    yanchor='top',
                    pad={"r": 10, "t": 10},
                    name="Month"
                )
            ]
        )
        return fig
    
    st.write("Bar and Line Chart")
    st.plotly_chart(create_bar_and_line_chart())
