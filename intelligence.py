import requests
import re
from transformers import pipeline

# ==========================================
# 1. LIVE DATA INGESTION (The Request)
# ==========================================
def fetch_live_html(url):
    """Sends a live request to a company website and downloads the HTML."""
    print(r"🌐 Sending handshake request to:", url)
    
    # We add a 'User-Agent' header so the website knows we are a modern browser
    # and doesn't mistake our script for a malicious bot.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        # Fetch the webpage
        response = requests.get(url, headers=headers, timeout=10)
        
        # If the website returns an error code (like 404 Not Found), stop here
        response.raise_for_status()
        
        print("✅ HTML downloaded successfully!")
        return response.text
        
    except Exception as e:
        print(f"❌ Failed to reach the website. Error: {e}")
        return None

# ==========================================
# 2. DATA CLEANING PIPELINE (Pre-processing)
# ==========================================
def clean_html(raw_html):
    """Strips out HTML elements to isolate human-readable text."""
    print("🧹 Filtering and cleaning text layers...")
    # Remove script and style tags completely so we don't read raw code/CSS
    clean_text = re.sub(r'<script.*?</script>', ' ', raw_html, flags=re.DOTALL)
    clean_text = re.sub(r'<style.*?</style>', ' ', clean_text, flags=re.DOTALL)
    
    # Strip out standard HTML tags
    clean_text = re.sub(r'<[^>]+>', ' ', clean_text)
    # Collapse extra spacing
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    return clean_text

# ==========================================
# 3. AI STRATEGY ENGINE
# ==========================================
def analyze_live_competitor(cleaned_text):
    print("🤖 Loading Zero-Shot Classification Model...")
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    
    # Custom business categories we want our AI to hunt for
    candidate_labels = [
        "E-Commerce & Retail",
        "Artificial Intelligence & Software",
        "Cloud Computing & Infrastructure",
        "Financial Services & Banking"
    ]
    
    print("🧠 Parsing live semantic patterns...")
    result = classifier(cleaned_text, candidate_labels)
    
    print("\n================ LIVE COMPETITOR ANALYSIS ================")
    print(f"Primary Business Track:   {result['labels'][0]} ({result['scores'][0]:.2%})")
    print(f"Secondary Business Track: {result['labels'][1]} ({result['scores'][1]:.2%})")
    print("==========================================================")

# ==========================================
# 4. EXECUTION
# ==========================================
if __name__ == "__main__":
    # Let's test a real, highly visible website address
    target_url = "https://news.ycombinator.com"
    
    # Step 1: Download live web data
    raw_html = fetch_live_html(target_url)
    
    if raw_html:
        # Step 2: Extract text from HTML layout
        cleaned_data = clean_html(raw_html)
        
        # Print a small snippet of what we extracted from the live site
        print(f"Extracted Live Snippet: {cleaned_data[:150]}...\n")
        
        # Step 3: Run it through the Transformer model
        analyze_live_competitor(cleaned_data)