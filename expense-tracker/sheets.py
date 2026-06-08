import gspread
from dotenv import load_dotenv
import os

class GoogleSheetsClient:
    def __init__(self):
        load_dotenv()
        self.gc = gspread.service_account(filename=os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
        spreadsheet = self.gc.open_by_key(os.environ["GOOGLE_SHEET_ID"])
        self.sheet = spreadsheet.worksheet("Notes de frais")
