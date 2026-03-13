import os
import json
import requests
import pandas as pd
import argparse
from datetime import datetime
import google.generativeai as genai

# ==============================================================================
# CONFIGURATION & SETUP
# ==============================================================================

# Constants
SAMPLE_DATA_FILE = "maritime_news_sample.json"
REPORT_OUTPUT_DIR = "reports"

def setup_gemini():
    """Configures the Gemini API Key."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable is not set.")
        print("Please set it using: set GEMINI_API_KEY=your_key")
        return False
    
    genai.configure(api_key=api_key)
    return True

# ==============================================================================
# STEP 1: COLLECT MARITIME NEWS
# ==============================================================================

def fetch_live_news(news_api_key):
    """Fetches live news from NewsAPI focused on maritime trade."""
    print("[*] Contacting NewsAPI for live global shipping news...")
    
    url = "https://newsapi.org/v2/everything"
    params = {
        'q': '("supply chain" OR "shipping port" OR "maritime trade" OR "port congestion" OR "canal blockage")',
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': 15,
        'apiKey': news_api_key
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        articles = data.get("articles", [])
        if not articles:
            print("[-] No live news found.")
            return []
            
        formatted_articles = []
        for article in articles:
            if article.get('title') and article.get('description'):
                formatted_articles.append({
                    "title": article['title'],
                    "description": article['description'],
                    "source": article.get('source', {}).get('name', 'Unknown'),
                    "date": article.get('publishedAt', '')[:10]
                })
        return formatted_articles
        
    except Exception as e:
        print(f"[!] Error fetching live news: {e}")
        return []

def load_offline_news():
    """Loads sample news data from a local JSON file (Demo Mode)."""
    print(f"[*] Loading offline news data from {SAMPLE_DATA_FILE}...")
    try:
        with open(SAMPLE_DATA_FILE, 'r') as f:
            data = json.load(f)
            # Format nicely for the prompt
            formatted_articles = []
            for item in data:
                 formatted_articles.append({
                     "title": item.get('title', ''),
                     "description": item.get('description', ''),
                     "source": item.get('source', 'Unknown'),
                     "date": item.get('publishedAt', '')[:10]
                 })
            return formatted_articles
    except FileNotFoundError:
        print(f"[!] Critical Error: Sample dataset '{SAMPLE_DATA_FILE}' not found.")
        print("[!] Please create it or run in live mode.")
        return []
    except json.JSONDecodeError:
        print(f"[!] Critical Error: Could not parse '{SAMPLE_DATA_FILE}'. Ensure it is valid JSON.")
        return []

# ==============================================================================
# STEP 2: PREPARE DATA
# ==============================================================================

def prepare_data_for_ai(articles):
    """Converts the list of articles into a structured prompt payload."""
    if not articles:
        return ""
        
    df = pd.DataFrame(articles)
    
    prompt_context = "RAW NEWS DATA:\n\n"
    for _, row in df.iterrows():
        prompt_context += f"- Title: {row['title']}\n"
        prompt_context += f"  Source: {row['source']} ({row['date']})\n"
        prompt_context += f"  Description: {row['description']}\n\n"
        
    return prompt_context

# ==============================================================================
# STEP 3 & 4: AI ANALYSIS & REPORT GENERATION
# ==============================================================================

def analyze_with_ai(news_context):
    """Passes the raw news to Gemini and asks for a structured intelligence report."""
    print("[*] Initializing MarineTrade Intelligence AI...")
    
    # Use gemini-1.5-flash which is widely available and fast
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    system_prompt = """
    You are an expert AI Researcher Agent for MarineTrade. Your job is to analyze raw maritime news and output a highly structured intelligence report.
    
    Filter out any irrelevant information and summarize the most critical insights.
    
    You MUST output EXACTLY in the following format. Do not add conversational intro/outro text.
    
    GLOBAL MARITIME INTELLIGENCE REPORT
    
    1. Port Disruptions
    [Summarize congestion, port closures, labor strikes, or operational delays based on the news.]
    
    2. Shipping Route Risks
    [Identify problems in major maritime routes.]
    
    3. Supply Chain Impact
    [Explain how these disruptions affect global trade and logistics.]
    
    4. Economic Trends
    [Identify trends affecting container shipping, oil shipping, or maritime trade.]
    
    5. Key Insights
    [Provide a short bullet-point summary of the most important events.]
    """
    
    full_prompt = f"{system_prompt}\n\n{news_context}"
    
    print("[*] AI is analyzing data and generating the report. Please wait...\n")
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        print(f"[!] Error during AI analysis: {e}")
        return "Report generation failed."

def save_report(report_text, mode):
    """Saves the output report to a text file for future Streamlit dashboard integration."""
    os.makedirs(REPORT_OUTPUT_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{REPORT_OUTPUT_DIR}/maritime_report_{mode}_{timestamp}.txt"
    
    with open(filename, "w", encoding='utf-8') as f:
        f.write(report_text)
        
    print(f"\n[+] Success! Report saved to: {filename}")
    print("[+] This data is now ready to be ingested by a Streamlit Dashboard.")

# ==============================================================================
# CLI INTERFACE
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="MarineTrade Intelligence AI Researcher Agent")
    parser.add_argument('--mode', choices=['live', 'demo'], default='demo', 
                        help="Run mode: 'live' uses NewsAPI, 'demo' uses local JSON data.")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print(" 🚢 MARINETRADE INTELLIGENCE AI - HACKATHON EDITION 🚢 ")
    print("=" * 60)
    print(f"Mode: {args.mode.upper()}\n")

    # 1. Check Gemini API
    if not setup_gemini():
        return

    # 2. Fetch News
    articles = []
    if args.mode == 'live':
        news_api_key = os.environ.get("NEWS_API_KEY")
        if not news_api_key:
            print("[!] Error: NEWS_API_KEY environment variable is missing.")
            print("[!] You need a News API Key to run in live mode. Download from newsapi.org")
            return
        articles = fetch_live_news(news_api_key)
    else:
        articles = load_offline_news()

    if not articles:
        print("[-] Exiting due to lack of data.")
        return

    # 3. Prepare Data
    news_context = prepare_data_for_ai(articles)

    # 4. Analyze and Generate Report
    report = analyze_with_ai(news_context)
    
    # Print the report to console
    print("\n\n" + report)
    
    # 5. Save the report
    save_report(report, args.mode)


if __name__ == "__main__":
    main()
