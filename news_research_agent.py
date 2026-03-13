import os
import requests
from newsapi import NewsApiClient
from google import genai
from google.genai import types

def fetch_maritime_news(news_api_key):
    """Fetches the latest news regarding shipping, ports, and supply chain logistics."""
    if not news_api_key:
         return "Error: Missing News API Key."
         
    print("\n[Research Agent] 📡 Scanning global news sources for maritime & supply chain updates...")
    newsapi = NewsApiClient(api_key=news_api_key)
    
    try:
        # Search for exact match phrases or broad keywords
        all_articles = newsapi.get_everything(
            q='("supply chain" OR "shipping port" OR "maritime trade" OR "ocean freight" OR "port congestion")',
            language='en',
            sort_by='publishedAt',
            page_size=10
        )
        
        if all_articles['status'] != 'ok':
            return f"Failed to fetch news. API Status: {all_articles['status']}"
            
        articles = all_articles.get('articles', [])
        
        if not articles:
            return "No recent news found for the specified queries."
            
        # Format the news for the AI to read easily
        formatted_news = "RECENT MARITIME & SUPPLY CHAIN NEWS:\n\n"
        for i, article in enumerate(articles, 1):
            source = article['source']['name']
            title = article['title']
            desc = article['description']
            date = article['publishedAt'][:10]
            
            # Skip empty articles
            if title and desc and source != '[Removed]':
                 formatted_news += f"--- Article {i} ---\n"
                 formatted_news += f"Source: {source} ({date})\n"
                 formatted_news += f"Title: {title}\n"
                 formatted_news += f"Summary: {desc}\n\n"
                 
        return formatted_news
        
    except Exception as e:
         return f"Error while fetching news: {str(e)}"

def analyze_shipping_news(gemini_api_key, news_data):
    """Uses Gemini to act as a Research Agent and analyze the raw news data."""
    if not gemini_api_key:
        return "Error: Missing Gemini API Key."
        
    print("[Research Agent] 🧠 Analyzing raw news data for supply chain impacts...")
    
    try:
        client = genai.Client(api_key=gemini_api_key)
        
        system_instruction = """
        You are an expert AI Research Agent specializing in Global Marine Trade, Logistics, and Supply Chain Risk Management.
        
        Your task is to read the provided raw news data and generate a structured, professional intelligence report.
        
        Focus Areas:
        1. Identify any disruptions (port congestion, strikes, weather events, geopolitical tensions).
        2. Highlight news specifically mentioning major ports or shipping channels.
        3. Filter out any noise or irrelevant news that happened to get caught in the keyword search.
        
        Output Format:
        - **Critical Disruptions:** (Highlight immediate threats to supply chains)
        - **Port & Logistics Updates:** (General operational news)
        - **Market & Economic Trends:** (Freight rates, carrier news, etc.)
        - **Agent Summary:** (A 2-3 sentence final verdict on the current state of maritime trade based solely on these articles)
        """
        
        prompt = f"Analyze the following real-time news data and structure it according to your directives:\n\n{news_data}"
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2, # Low temperature for factual analysis
            )
        )
        return response.text
        
    except Exception as e:
         return f"Error during Gemini analysis: {str(e)}"


if __name__ == "__main__":
    print("="*50)
    print("🚢 SUPPLY CHAIN RESEARCH AGENT INITIALIZED")
    print("="*50)
    
    # Needs both keys to function end-to-end
    NEWS_API_KEY = os.environ.get("NEWS_API_KEY") 
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    
    if not NEWS_API_KEY or not GEMINI_API_KEY:
        print("\n❌ MISSING CREDENTIALS!")
        print("To run this agent, you must set both environment variables:")
        print("set NEWS_API_KEY=your_key_here")
        print("set GEMINI_API_KEY=your_key_here")
        print("\nYou can get a free News API key at: https://newsapi.org/")
    else:
        # Step 1: Fetch raw data
        raw_news = fetch_maritime_news(NEWS_API_KEY)
        
        if "RECENT MARITIME" in raw_news:
            # Step 2: Analyze data
            analysis_report = analyze_shipping_news(GEMINI_API_KEY, raw_news)
            
            print("\n" + "="*50)
            print("📑 FINAL INTELLIGENCE REPORT")
            print("="*50 + "\n")
            print(analysis_report)
        else:
            print("\nAgent stopped: Could not fetch valid news data. Log:")
            print(raw_news)
