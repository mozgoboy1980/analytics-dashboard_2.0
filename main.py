from fastapi import FastAPI
from data.ga4_collector import fetch_ga4_data
from storage.save_to_sheets import save_to_sheet

app = FastAPI()

@app.get("/run-ga4")
def run_collection():
    data = fetch_ga4_data()
    save_to_sheet(data)
    return {"status": "ok", "rows": len(data)}
