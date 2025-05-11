import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

VALID_MODELS = {
    "gemini-1.5-pro-latest": "Most capable model",
    "gemini-1.5-flash-latest": "Fastest model",
    "gemini-pro": "Original model"
}

def extract_card_info(source: str, context: dict, model_name: str = "gemini-1.5-flash-latest") -> list:
    """Extract credit card info from content using Gemini"""
    try:
        model = genai.GenerativeModel(model_name)
        
        prompt = f"""
        Analyze this content and extract ALL AVAILABLE credit card information:
        {json.dumps(context, indent=2)}
        
        Return ONLY THE FIELDS THAT CONTAIN INFORMATION in this JSON format:
        {{
          "cards": [
            {{
              // ONLY INCLUDE FIELDS THAT HAVE DATA
              "card_name": "Name if available",
              "issuing_bank": "Bank if available",
              "fees": {{
                // Include only present fee types
                "annual": "Amount if available",
                "joining": "Amount if available"
              }},
              "rewards": [
                // Only include if rewards exist
                "Reward 1 details",
                "Reward 2 details"
              ],
              "benefits": [
                // Only include if benefits exist
                "Benefit 1",
                "Benefit 2"
              ],
              "eligibility": "Criteria if available",
              "source": "{source}"
            }}
          ]
        }}
        """
        
        response = model.generate_content(prompt)
        response_text = clean_response_text(response.text)
        data = json.loads(response_text)
        
        # Remove empty fields
        return [remove_empty_fields(card) for card in data.get("cards", [])]
    
    except Exception as e:
        raise Exception(f"Gemini processing failed: {str(e)}")

def remove_empty_fields(card: dict) -> dict:
    """Remove empty/null fields from card data"""
    return {k: v for k, v in card.items() if v not in [None, "", [], {}]}

def clean_response_text(text: str) -> str:
    """Clean Gemini's response text"""
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    return text.strip()