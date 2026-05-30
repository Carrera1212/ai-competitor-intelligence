import requests
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

# 1. Initialize the FastAPI Application Instance
app = FastAPI(title="Live Competitor Intelligence API")

# 2. Pre-load the AI Model Once when the server boots up
print("🤖 Booting up Neural Network Engine...")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
print("🚀 AI Model Loaded and Ready!")

# 3. Define what the incoming request payload data should look like
class URLPayload(BaseModel):
    url: str

# 4. Core Processing Helper Functions (From your working logic)
def fetch_live_html(url: str):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception:
        return None

def clean_html(raw_html: str):
    clean_text = re.sub(r'<script.*?</script>', ' ', raw_html, flags=re.DOTALL)
    clean_text = re.sub(r'<style.*?</style>', ' ', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'<[^>]+>', ' ', clean_text)
    return re.sub(r'\s+', ' ', clean_text).strip()

# 5. Create the Interactive Live API Endpoint
@app.post("/analyze")
def analyze_endpoint(payload: URLPayload):
    # Step A: Download data from the dynamic user-provided URL
    raw_html = fetch_live_html(payload.url)
    
    if not raw_html:
        # If the URL fails, throw a formal HTTP 400 bad request error back to the user
        raise HTTPException(status_code=400, detail="Could not retrieve or read the provided URL.")
    
    # Step B: Clean the data
    cleaned_data = clean_html(raw_html)
    
    # Step C: Dynamic AI Classification
    candidate_labels = [
        "E-Commerce & Retail",
        "Artificial Intelligence & Software",
        "Cloud Computing & Infrastructure",
        "Financial Services & Banking"
    ]
    result = classifier(cleaned_data, candidate_labels)
    
    # Step D: Hand back a beautiful, structured JSON response
    return {
        "target_url": payload.url,
        "primary_track": result['labels'][0],
        "confidence": f"{result['scores'][0]:.2%}",
        "raw_text_snippet": f"{cleaned_data[:100]}..."
    }

# 6. A basic landing health check
# ==========================================
# 6. RUNTIME CONTROLLER (Forces Port 8000 Open)
# ==========================================
if __name__ == "__main__":
    import uvicorn
    print("📡 Forcing network gates open on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)