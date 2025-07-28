from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from typing import Optional
from data.ga4_collector import fetch_total_ga4_data as fetch_ga4_data
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
        <button type="submit">Собрать и скачать CSV</button>
      </form>
    </body>
    </html>
    """

@app.post("/", response_class=StreamingResponse)
def process_form(
    start: str = Form(...),
    end: str = Form(...)
):
    metrics = ["activeUsers", "sessions", "screenPageViews"]
    data = fetch_ga4_data(start, end, metrics)

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Google Analytics:", f"{start} — {end}"])
    writer.writerow(["Web page unique users", data[0]])
    writer.writerow(["Sessions", data[1]])
    writer.writerow(["Pageviews", data[2]])

    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=ga4_summary.csv"
    })
