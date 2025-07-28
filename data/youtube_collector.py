import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/yt-analytics.readonly"]
CLIENT_SECRET_FILE = os.getenv("YOUTUBE_CLIENT_SECRET_PATH", "credentials/client_secret_youtube.json")
TOKEN_FILE = "credentials/youtube_token.json"

def get_authenticated_service():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return build("youtubeAnalytics", "v2", credentials=creds)

def fetch_youtube_data(start_date="2025-07-01", end_date="2025-07-28"):
    service = get_authenticated_service()
    response = service.reports().query(
        ids="channel==MINE",
        startDate=start_date,
        endDate=end_date,
        metrics="views,estimatedMinutesWatched,averageViewDuration,subscribersGained"
    ).execute()

    # Преобразуем в словарь {название: значение}
    headers = response["columnHeaders"]
    values = response["rows"][0] if "rows" in response else [0] * len(headers)

    return {h["name"]: v for h, v in zip(headers, values)}
