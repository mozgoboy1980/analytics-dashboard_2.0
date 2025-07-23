import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config.settings import SHEETS_KEY, SHEETS_CREDS_FILE

def save_to_sheet(data):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(SHEETS_CREDS_FILE, scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(SHEETS_KEY).worksheet("GA4")
    sheet.clear()
    sheet.update("A1", [["Page Title", "Page Path", "Users", "Engagement Rate"]] + data)
