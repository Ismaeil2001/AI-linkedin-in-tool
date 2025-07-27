# test_google_sheet.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

sheet = client.open("LinkedIn Leads").sheet1  # Change if your sheet has a different name
print("✅ Connected to sheet:", sheet.title)
