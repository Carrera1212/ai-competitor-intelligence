import re
import sqlite3
from datetime import datetime
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

# 1. Initialize FastAPI Application Instance
app = FastAPI(title="Production Competitor Intelligence Engine")

# 2. Database Core Setup Configuration
DB_FILE = "competitor_data.db"

def init_db():
    """Executes on system boot to establish our SQL data table structure."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competitor_insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            primary_track TEXT NOT NULL,
            confidence TEXT NOT NULL,
            scan_date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Initialize the database immediately
init_db()

# 3. Pre-load the AI Model Layer
print("🤖 Loading Transformer Model into memory...")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
print("🚀 Model Engine Successfully Initialized!")

class URLPayload(BaseModel):
    url: str

# 4. Ingestion & Cleaning Helpers
def fetch_and_clean(url: str):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        clean_text = re.sub(r'<script.*?</script>', ' ', response.text, flags=re.DOTALL)
        clean_text = re.sub(r'<style.*?</style>', ' ', clean_text, flags=re.DOTALL)
        clean_text = re.sub(r'<[^>]+>', ' ', clean_text)
        return re.sub(r'\s+', ' ', clean_text).strip()
    except Exception:
        return None

# 5. Endpoint A: Process, Analyze, AND Write to SQL Table
@app.post("/analyze")
def analyze_and_store(payload: URLPayload):
    cleaned_data = fetch_and_clean(payload.url)
    if not cleaned_data:
        raise HTTPException(status_code=400, detail="Failed to read website layout.")
    
    # Run the Deep Learning Classify Step
    candidate_labels = [
        "E-Commerce & Retail", 
        "Artificial Intelligence & Software", 
        "Cloud Computing & Infrastructure", 
        "Financial Services & Banking"
    ]
    result = classifier(cleaned_data, candidate_labels)
    
    primary_track = result['labels'][0]
    confidence_score = f"{result['scores'][0]:.2%}"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 💾 --- SQL DATABASE INTERACTION LAYER ---
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO competitor_insights (url, primary_track, confidence, scan_date)
        VALUES (?, ?, ?, ?)
    """, (payload.url, primary_track, confidence_score, current_time))
    conn.commit()
    conn.close()
    # ------------------------------------------
    
    return {
        "status": "Success",
        "message": "Analysis committed directly to database storage!",
        "url": payload.url,
        "ai_analysis": {"track": primary_track, "confidence": confidence_score}
    }

# 6. Endpoint B: Read Historical Audit Records
@app.get("/history")
def get_historical_scans():
    """Queries the SQLite database to fetch every single historical record saved."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT url, primary_track, confidence, scan_date FROM competitor_insights ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    # Map the raw database tuples into structured JSON objects for the browser
    history = []
    for row in rows:
        history.append({
            "url": row[0],
            "primary_track": row[1],
            "confidence": row[2],
            "scan_date": row[3]
        })
    return {"total_saved_scans": len(history), "history_log": history}

# 7. Runtime Controller Link
if __name__ == "__main__":
    import uvicorn
    print("📡 Forcing persistent network gates open on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)