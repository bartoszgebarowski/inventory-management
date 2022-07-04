import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("Inventory Management")

class WorksheetNotFoundError(Exception):
    pass


def get_all_worksheets_titles() -> list:
    """
    Function that returns the list of all worksheets titles
    """
    worksheet_list = SHEET.worksheets()
    worksheets_all = []
    for index in range(len(worksheet_list)):
        worksheets_all.append(worksheet_list[index].title)
    return worksheets_all


def print_all_worksheets():
    """
    Function that prints all worksheets in the spreadsheet to the terminal
    """
    for sheet in get_all_worksheets_titles():
        print(sheet)

def validate_user_chosen_sheet(input_candidate: str) -> str:
    """
    Function that checks if user input exist as a worksheet
    """
    user_input_lower = input_candidate.lower()
    words_to_check = get_all_worksheets_titles()
    worksheets_names = [word for word in words_to_check if word.lower() == user_input_lower]
    try:
        return worksheets_names[0]
    except IndexError:
        raise WorksheetNotFoundError
    
def delete_worksheet():
    """
    Function that delete worksheet from a spreadsheet
    """
    user_input = input('Enter the worksheet name to delete: ')
    try:
        worksheet_name = validate_user_chosen_sheet(user_input)
    except WorksheetNotFoundError:
        print('Worksheet not found')
        return
    if len(get_all_worksheets_titles()) > 1:
        print('Processing ...')
        sheet_to_remove = SHEET.worksheet(worksheet_name)
        SHEET.del_worksheet(sheet_to_remove)
        print('Sheet successfully removed !')
    elif len(get_all_worksheets_titles()) == 1:
        print("You can't delete all the sheets in a spreadsheet.")
    else:
        print('Could not remove worksheet')

delete_worksheet()