import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS_FILE = "credentials/ecopurify-dashboard-b6d7956c63c6.json"

creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

sheet = client.open_by_key("1_NdtVkGrwzdqNms2D5xIDiR18QC6gubPBZJshauDKLo").worksheet("customers")

data = sheet.get_all_records()
print(data)
