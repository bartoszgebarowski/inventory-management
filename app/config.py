import gspread
from google.oauth2.service_account import Credentials


class Config:

    SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

    CREDS = Credentials.from_service_account_file("creds.json")
    SCOPED_CREDS = CREDS.with_scopes(SCOPE)
    GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
    SHEET = GSPREAD_CLIENT.open("Inventory Management")
    MAX_KEYS = 6

    def __init__(self) -> None:
        self._current_worksheet = None

    @property
    def current_worksheet(self):
        return self._current_worksheet

    @current_worksheet.setter
    def current_worksheet(self, worksheet_name: str):
        self._current_worksheet = worksheet_name
