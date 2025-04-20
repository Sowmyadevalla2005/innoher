# data_collector.py
import os
import requests
import pandas as pd
from dotenv import load_dotenv
import datetime

# Load environment variables
load_dotenv()

class DataCollector:
    def __init__(self):
        self.weather_api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        self.news_api_key = os.getenv("NEWSAPI_API_KEY")
        
    def fetch_weather_data(self, cities=None):
        """Fetch weather data for specified cities"""
        if cities is None:
            cities = ["London", "New York", "Tokyo", "Paris", "Beijing"]
            
        weather_data = []
        
        for city in cities:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                weather_data.append({
                    'city': city,
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'weather_condition': data['weather'][0]['main'],
                    'timestamp': datetime.datetime.now().isoformat()
                })
                
        df = pd.DataFrame(weather_data)
        df.to_csv("data/weather_data.csv", index=False)
        return df
    
    def fetch_climate_news(self, keywords=None):
        """Fetch news related to climate and insurance"""
        if keywords is None:
            keywords = "climate change insurance risk TNFD"
            
        url = f"https://newsapi.org/v2/everything?q={keywords}&apiKey={self.news_api_key}&pageSize=100"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            news_data = []
            
            for article in data.get('articles', []):
                news_data.append({
                    'title': article.get('title'),
                    'source': article.get('source', {}).get('name'),
                    'author': article.get('author'),
                    'description': article.get('description'),
                    'content': article.get('content'),
                    'url': article.get('url'),
                    'published_at': article.get('publishedAt'),
                    'timestamp': datetime.datetime.now().isoformat()
                })
                
            df = pd.DataFrame(news_data)
            df.to_csv("data/climate_news.csv", index=False)
            return df
            
    def save_data(self):
        """Ensure data directory exists and save all data"""
        os.makedirs("data", exist_ok=True)
        
        print("Fetching weather data...")
        weather_df = self.fetch_weather_data()
        print(f"Saved {len(weather_df)} weather records")
        
        print("Fetching climate news...")
        news_df = self.fetch_climate_news()
        print(f"Saved {len(news_df)} news articles")
        
        return {"weather": weather_df, "news": news_df}