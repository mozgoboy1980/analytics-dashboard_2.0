from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from typing import List, Optional
from data.ga4_collector import fetch_ga4_data
import csv
import io

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def dashboard_form():
    return """
    <html>
    <head><title>GA4 Dashboard</title></head>
    <body>
      <h2>Сбор данных из GA4</h2>
      <form method="post">
        <label>Дата начала: <input type="date" name="start"></label><br><br>
        <label>Дата окончания: <input type="date" name="end"></label><br><br>

        <label><input type="checkbox" name="metrics" value="activeUsers" checked> activeUsers</label><br>
        <label><input type="checkbox" name="metrics" value="engagementRate" checked> engagementRate</label><br>
        <label><input type="checkbox" name="metrics" value="sessions"> sessions</label><br><br>

        <button type="submit">Собрать и скачать CSV</button>
      </form>
    </body>
    </html>
    """

@app.post("/", response_class=StreamingResponse)
def process_form(
    start: str = Form(...),
    end: str = Form(...),
    metrics: Optional[List[str]] = Form(None)
):
    metrics = metrics or []
    data = fetch_ga4_data(start, end, metrics)
    output = io.StringIO()
    writer = csv.writer(output)
    headers = ["Page Title", "Page Path"] + metrics
    writer.writerow(headers)
    for row in data:
        writer.writerow(row)
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=ga4_export.csv"
    })
