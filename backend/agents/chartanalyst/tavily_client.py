# backend/agents/chartanalyst/tavily_client.py
import os
import requests

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def get_web_insights(query: str) -> str:
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "advanced",
        "include_answer": True,
    }
    res = requests.post(url, json=payload)
    if res.status_code == 200:
        return res.json().get("answer", "")
    return "No web insights found."
