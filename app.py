import streamlit as st
from utils.llm_processor import extract_card_info, VALID_MODELS
from utils.serper_processor import get_website_data
from utils.pdf_processor import extract_text_from_pdf
from dotenv import load_dotenv
import tempfile
import os

load_dotenv()

def display_results(cards):
    """Dynamically display only available card information"""
    if not cards:
        st.warning("No credit card information found")
        return
    
    st.success(f"Found {len(cards)} card(s)")
    
    for card in cards:
        with st.expander(f"💳 {card.get('card_name', 'Unnamed Card')}"):
            # Card Header
            cols = st.columns([1,2])
            with cols[0]:
                if 'issuing_bank' in card:
                    st.markdown(f"**Issuing Bank:** {card['issuing_bank']}")
            
            # Fees Section (only if exists)
            if 'fees' in card:
                st.subheader("Fees", divider='gray')
                fee_cols = st.columns(3)
                if 'annual' in card['fees']:
                    fee_cols[0].metric("Annual Fee", card['fees']['annual'])
                if 'joining' in card['fees']:
                    fee_cols[1].metric("Joining Fee", card['fees']['joining'])
            
            # Rewards Section (only if exists)
            if 'rewards' in card and card['rewards']:
                st.subheader("Rewards", divider='gray')
                for reward in card['rewards']:
                    st.markdown(f"- {reward}")
            
            # Benefits Section (only if exists)
            if 'benefits' in card and card['benefits']:
                st.subheader("Benefits", divider='gray')
                for benefit in card['benefits']:
                    st.markdown(f"- {benefit}")
            
            # Eligibility (only if exists)
            if 'eligibility' in card:
                st.subheader("Eligibility", divider='gray')
                st.write(card['eligibility'])
            
            # Source
            if 'source' in card:
                st.caption(f"Source: {card['source']}")

# Main app configuration
st.set_page_config(page_title="💳 Credit Card Extractor", layout="wide")
st.title("💳 AI-Powered Credit Card Extractor")

# Model selection in sidebar
with st.sidebar:
    st.subheader("Settings")
    model_name = st.selectbox(
        "Gemini Model",
        options=list(VALID_MODELS.keys()),
        index=1,
        help=VALID_MODELS["gemini-1.5-flash-latest"]
    )
    
    input_type = st.radio(
        "Input Type",
        ["Website URL", "PDF File"],
        index=0
    )

# Main content area
if input_type == "Website URL":
    url = st.text_input("Enter Credit Card Page URL", placeholder="https://www.bankname.com/credit-cards")
    
    if st.button("Extract from Website"):
        if not url.startswith(('http://', 'https://')):
            st.warning("Please enter a valid URL")
            st.stop()
        
        with st.spinner(f"Analyzing website with {model_name}..."):
            try:
                search_data = get_website_data(url)
                cards = extract_card_info(url, search_data, model_name)
                display_results(cards)
            except Exception as e:
                st.error(f"Error: {str(e)}")

else:  # PDF File
    uploaded_file = st.file_uploader("Upload PDF File", type=["pdf"])
    
    if uploaded_file and st.button("Extract from PDF"):
        with st.spinner(f"Analyzing PDF with {model_name}..."):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    pdf_path = tmp.name
                
                text_content = extract_text_from_pdf(pdf_path)
                cards = extract_card_info("PDF Document", {"content": text_content}, model_name)
                display_results(cards)
            except Exception as e:
                st.error(f"Error: {str(e)}")
            finally:
                if os.path.exists(pdf_path):
                    os.unlink(pdf_path)