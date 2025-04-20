# main.py
import os
import argparse
from data_collector import DataCollector
from data_processor import DataProcessor
from climate_agent import ClimateRiskAgent

def main():
    parser = argparse.ArgumentParser(description="Climate Risk Agent for Insurance Industry")
    parser.add_argument("--collect", action="store_true", help="Collect new data")
    parser.add_argument("--process", action="store_true", help="Process collected data")
    parser.add_argument("--report", action="store_true", help="Generate risk report")
    args = parser.parse_args()
    
    # Create necessary directories
    os.makedirs("data", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    
    if args.collect or not args.process and not args.report:
        print("Step 1: Collecting data...")
        collector = DataCollector()
        data = collector.save_data()
        print("Data collection complete!")
        
    if args.process or not args.collect and not args.report:
        print("Step 2: Processing data...")
        processor = DataProcessor()
        processed_data = processor.process_data()
        print("Data processing complete!")
        
    if args.report or not args.collect and not args.process:
        print("Step 3: Generating risk report...")
        agent = ClimateRiskAgent()
        report = agent.generate_risk_report()
        print("Risk report generated!")
        print(f"Report saved to: {os.path.abspath('reports/climate_risk_report.md')}")
        
    print("All tasks completed!")

if __name__ == "__main__":
    main()