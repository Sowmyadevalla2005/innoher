# data_processor.py
import pandas as pd
import os
from transformers import pipeline

class DataProcessor:
    def __init__(self):
        # Initialize sentiment analysis pipeline
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        
    def load_data(self):
        """Load data from CSV files"""
        weather_df = pd.read_csv("data/weather_data.csv")
        news_df = pd.read_csv("data/climate_news.csv")
        return weather_df, news_df
        
    def analyze_news_sentiment(self, news_df=None):
        """Analyze sentiment of news articles"""
        if news_df is None:
            news_df = pd.read_csv("data/climate_news.csv")
            
        # Only process rows with content
        news_df = news_df.dropna(subset=["description"])
        
        # Analyze sentiment of description (process in batches to avoid memory issues)
        sentiments = []
        batch_size = 10
        
        for i in range(0, len(news_df), batch_size):
            batch = news_df["description"].iloc[i:i+batch_size].tolist()
            batch_sentiments = self.sentiment_analyzer(batch)
            sentiments.extend(batch_sentiments)
        
        # Add sentiment to dataframe
        news_df["sentiment"] = [item["label"] for item in sentiments]
        news_df["sentiment_score"] = [item["score"] for item in sentiments]
        
        # Save processed data
        news_df.to_csv("data/processed_news.csv", index=False)
        return news_df
        
    def process_data(self):
        """Process all data"""
        os.makedirs("data", exist_ok=True)
        
        print("Processing news data for sentiment...")
        processed_news_df = self.analyze_news_sentiment()
        print(f"Processed {len(processed_news_df)} news articles")
        
        return {"processed_news": processed_news_df}