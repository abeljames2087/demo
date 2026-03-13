import os
import json
import requests
from google import genai
from google.genai import types

def search_marine_news(query):
    """Simulated function to fetch real-time marine news. In a real app, this would use NewsAPI or similar."""
    print(f"Searching for real-time marine news about: {query}")
    # Returning mock real-time data for demonstration
    return [
        {"title": "Suez Canal Traffic Down 40% Due to Red Sea Tensions", "source": "Maritime Executive", "date": "Today"},
        {"title": "Port of LA Reports Record Breaking Volume in Q3", "source": "Supply Chain Dive", "date": "Yesterday"},
        {"title": "New Emissions Regulations to Hit Old Fleets Hard", "source": "Lloyd's List", "date": "2 Days Ago"}
    ]

def get_port_status(port_name):
    """Simulated function to check congestion at a major port."""
    print(f"Checking congestion at {port_name}...")
    statuses = {
        "Port of LA": "High Congestion - 4 Days berthing delay",
        "Singapore": "Normal Operations",
        "Rotterdam": "Minor Weather Delays",
        "Shanghai": "High Volume - 2 Days delay"
    }
    return statuses.get(port_name, "Status Unknown")

def run_research_agent(prompt: str, api_key: str):
    """Runs the Research Agent using the Gemini API."""
    if not api_key:
        return "Error: GEMINI_API_KEY environment variable not set. Please set it to run the live agent."
        
    try:
        client = genai.Client(api_key=api_key)
        
        # Tools the agent can use
        marine_tools = [search_marine_news, get_port_status]
        
        system_instruction = """
        You are an expert AI Research Agent specializing in Global Marine Trade and Maritime Economics.
        Your task is to conduct deep research and provide structured insights about global marine trade.
        You have access to tools to fetch real-time news and port statuses. Use them if the user asks about current conditions.
        
        Focus areas: Global shipping routes, Key ports, Commodities, Trends (geopolitics, disruptions), Tech, Environment.
        Provide clear headings, mention important organizations (IMO, WTO), and maintain a professional, analytical tone.
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=marine_tools,
                temperature=0.2,
            )
        )
        return response.text
        
    except Exception as e:
        return f"Agent encountered an error: {str(e)}"

# Example Usage (can be run directly from terminal for testing)
if __name__ == "__main__":
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        print("Starting Research Agent...")
        result = run_research_agent("What is the current status of the Port of LA and recent news regarding the Suez Canal?", api_key)
        print("\n--- Agent Report ---\n")
        print(result)
    else:
        print("Please set the GEMINI_API_KEY environment variable to test the agent.")
