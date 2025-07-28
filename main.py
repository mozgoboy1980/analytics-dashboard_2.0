from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from typing import Optional
from data.ga4_collector import fetch_total_ga4_data
from data.youtube_collector import fetch_youtube_data
import csv
import io

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def dashboard_form():
    return """
    <html>
    <head><title>Dashboard</title></head>
    <body>
      <h2>Сбор данных</h2>

      <h3>Сайт</h3>
      <form method="post" action="/download-site">
        <label>Дата начала: <input type="date" name="start"></label><br><br>
        <label>Дата окончания: <input type="date" name="end"></label><br><br>
        <button type="submit">Скачать сайт CSV</button>
      </form>

      <h3>YouTube</h3>
      <form method="post" action="/download-youtube">
        <button type="submit">Скачать YouTube CSV</button>
      </form>
    </body>
    </html>
    """

@app.post("/download-site", response_class=StreamingResponse)
def download_site(start: str = Form(...), end: str = Form(...)):
    metrics = ["activeUsers", "sessions", "screenPageViews"]
    data = fetch_total_ga4_data(start, end, metrics)

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

@app.post("/download-youtube", response_class=StreamingResponse)
def download_youtube():
    yt_data = fetch_youtube_data()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["YouTube Summary"])
    for key, value in yt_data.items():
        writer.writerow([key, value])

    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=youtube_summary.csv"
    })
