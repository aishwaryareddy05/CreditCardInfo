import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def get_website_data(url: str) -> dict:
    """Get website content using Serper API's URL inspection feature"""
    if not SERPER_API_KEY:
        raise ValueError("SERPER_API_KEY not found in environment variables")

    payload = {
        "q": f"site:{url} credit card",
        "gl": "in",  # Country code for India
        "hl": "en"   # Language
    }
    
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            "https://google.serper.dev/search",
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise Exception(f"Serper API request failed: {str(e)}")