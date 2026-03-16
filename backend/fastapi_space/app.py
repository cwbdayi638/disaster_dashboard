from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI(title="防災即時資訊 API", description="提供即時災情數據", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_URL = "https://raw.githubusercontent.com/cwbdayi638/disaster_dashboard/main/data/reports.json"

def load_data():
    try:
        response = requests.get(DATA_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error loading data: {e}")
        return []

@app.get("/")
def read_root():
    return {
        "status": "ok", 
        "message": "災情即時資訊 API 服務運行中",
        "endpoints": ["/reports", "/stats"]
    }

@app.get("/reports")
@app.get("/api/reports")
def get_reports(severity: str = None):
    data = load_data()
    if severity:
        return [r for r in data if r.get('incident', {}).get('severity') == severity]
    return data

@app.get("/stats")
@app.get("/api/stats")
def get_stats():
    data = load_data()
    stats = {}
    for r in data:
        sev = r.get('incident', {}).get('severity', 'Unknown')
        stats[sev] = stats.get(sev, 0) + 1
    return {"total": len(data), "severity_distribution": stats}
