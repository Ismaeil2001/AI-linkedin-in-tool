import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# Define the scopes
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scopes)
client = gspread.authorize(creds)

# Open the spreadsheet and worksheet
SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "LinkedIn Leads")
WORKSHEET_NAME = os.getenv("GOOGLE_WORKSHEET_NAME", "Sheet1")
sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)

def append_to_google_sheet(timestamp, profile_name, profile_url, text, score, action):
    try:
        row = [timestamp, profile_name, profile_url, text, score, action]
        sheet.append_row(row)
        print("✅ Logged to Google Sheets")
    except Exception as e:
        print(f"❌ Google Sheets Append Error: {e}")
