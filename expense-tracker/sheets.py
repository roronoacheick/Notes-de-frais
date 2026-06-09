import io
import os
from datetime import datetime
import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

class GoogleSheetsClient:
    def __init__(self):
        creds = Credentials.from_service_account_file(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"], scopes=SCOPES)
        self.gc = gspread.authorize(creds)
        spreadsheet = self.gc.open_by_key(os.environ["GOOGLE_SHEET_ID"])
        self.sheet = spreadsheet.worksheet("Notes de frais")
        self.drive = build("drive", "v3", credentials=creds)

    def upload_image_to_drive(self, image_bytes: bytes, filename: str, media_type: str) -> str:
        media = MediaIoBaseUpload(io.BytesIO(image_bytes), mimetype=media_type, resumable=False)
        file = (self.drive.files().create(body={"name": filename}, media_body=media, fields="id").execute())
        file_id = file["id"]

        self.drive.permissions().create(fileId=file_id, body={"type": "anyone", "role": "reader"}).execute()
        return f"https://drive.google.com/uc?id={file_id}"

    def append_expense(self, data: dict, image_url: str = None) -> None:
        image_formula = f'=IMAGE("{image_url}")' if image_url else ""
                    
        row = [
            datetime.now().strftime("%d/%m/%Y %H:%M:%S"),  
            data.get("categorie"),                          
            data.get("fournisseur"),                        
            data.get("date"),                               
            data.get("montant_ttc"),                       
            data.get("tva"),                                
            data.get("devise", "EUR"),                      
            data.get("description"),                        
            data.get("confiance"),                        
            image_formula                                 
        ]
        self.sheet.append_row(row, value_input_option="USER_ENTERED")