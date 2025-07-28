from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from typing import Optional
from data.ga4_collector import fetch_ga4_data
from data.youtube_collector import fetch_youtube_data
import csv
import io

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def dashboard_form():
    return """
    <html>
    <head><title>Сбор данных</title></head>
    <body>
      <h2>Сбор данных</h2>
      <form method="post">
        <h3>Период</h3>
        <label>Дата начала: <input type="date" name="start"></label><br><br>
        <label>Дата окончания: <input type="date" name="end"></label><br><br>
        <button type="submit">Собрать и скачать CSV</button>
      </form>
    </body>
    </html>
    """

@app.post("/", response_class=StreamingResponse)
def process_form(start: str = Form(...), end: str = Form(...)):
    output = io.StringIO()
    writer = csv.writer(output)

    # --- Google Analytics ---
    metrics = ["activeUsers", "sessions", "screenPageViews"]
    ga_data = fetch_ga4_data(start, end, metrics)

    totals = [0] * len(metrics)
    for row in ga_data:
        for i in range(len(metrics)):
            totals[i] += int(row[2 + i])

    writer.writerow(["Google Analytics:", f"{start} — {end}"])
    writer.writerow(["Web page unique users", totals[0]])
    writer.writerow(["Sessions", totals[1]])
    writer.writerow(["Pageviews", totals[2]])
    writer.writerow([])

    # --- YouTube Analytics ---
    yt_response = fetch_youtube_data(start, end)
    rows = yt_response.get("rows", [])
    headers = yt_response.get("columnHeaders", [])

    writer.writerow(["YouTube:", f"{start} — {end}"])
    header_names = [h["name"] for h in headers]
    writer.writerow(header_names)
    for row in rows:
        writer.writerow(row)

    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=analytics_report.csv"
    })
