import pdfplumber
from typing import Optional
import re

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text content from PDF file"""
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
        
        # Clean up text
        text = re.sub(r'\n{3,}', '\n\n', text)  # Remove excessive newlines
        return text.strip()
    
    except Exception as e:
        raise Exception(f"PDF extraction failed: {str(e)}")