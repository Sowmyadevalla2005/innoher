# climate_agent.py
import os
import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import torch

class ClimateRiskAgent:
    def __init__(self):
        # Load model for risk classification
        self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        
        # For demonstration - normally you would fine-tune this model
        self.model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=3)
        
        # Create classification pipeline for risk assessment
        self.risk_classifier = pipeline(
            "text-classification", 
            model=self.model, 
            tokenizer=self.tokenizer,
            return_all_scores=True
        )
        
        # Create summarization pipeline
        self.summarizer = pipeline("summarization")
        
    def assess_climate_risk(self, text):
        """Assess climate risk level from text"""
        # This is a placeholder - in a real application, you'd use a fine-tuned model
        risk_scores = self.risk_classifier(text)
        return risk_scores
        
    def generate_risk_report(self, news_df=None):
        """Generate risk report based on processed news data"""
        if news_df is None:
            news_df = pd.read_csv("data/processed_news.csv")
            
        # Filter for high-risk news (based on negative sentiment as a proxy)
        high_risk_news = news_df[news_df["sentiment"] == "NEGATIVE"]
        
        # Compile report content
        report_content = "# Climate Risk Report for Insurance Industry\n\n"
        report_content += f"## Executive Summary\n\n"
        report_content += f"Analysis of {len(news_df)} news articles identified {len(high_risk_news)} high-risk climate events.\n\n"
        
        # Add top risks
        report_content += "## Top Climate Risks\n\n"
        
        for i, (_, article) in enumerate(high_risk_news.sort_values("sentiment_score").head(5).iterrows()):
            report_content += f"### {i+1}. {article['title']}\n\n"
            report_content += f"**Source:** {article['source']}\n\n"
            report_content += f"**Description:** {article['description']}\n\n"
            
            # Generate risk assessment
            risk_assessment = "High risk due to potential impact on insurance claims and policy premiums."
            report_content += f"**Risk Assessment:** {risk_assessment}\n\n"
            
        # Save report
        os.makedirs("reports", exist_ok=True)
        with open("reports/climate_risk_report.md", "w") as f:
            f.write(report_content)
            
        return report_content
        
    def summarize_article(self, article_text):
        """Summarize a news article"""
        summary = self.summarizer(article_text, max_length=100, min_length=30, do_sample=False)
        return summary[0]['summary_text']