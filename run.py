import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate

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


class SpreadSheetNotFoundError(Exception):
    pass


current_worksheet = "Copy of Stock"


def get_all_worksheets_titles() -> list:
    """
    Function that returns the list of all worksheets titles
    """
    worksheet_list = SHEET.worksheets()
    worksheets_all = []
    for index in range(len(worksheet_list)):
        worksheets_all.append(worksheet_list[index].title)
    return worksheets_all


def check_if_worksheet_exist(input_candidate) -> bool:
    """
    Function that checks if worksheet exist
    """
    user_input_lower = input_candidate.lower()
    words_to_check = get_all_worksheets_titles()
    worksheets_names = [
        word for word in words_to_check if word.lower() == user_input_lower
    ]
    return bool(worksheets_names)


def get_all_worksheets_titles_with_id() -> dict:
    """
    Function that returns the list of all worksheets titles
    """
    worksheets = SHEET.worksheets()
    worksheets_titles_with_id = {}
    for worksheet in worksheets:
        worksheets_titles_with_id[worksheet.title] = [worksheet.id]
    return worksheets_titles_with_id


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
    worksheets_names = [
        word for word in words_to_check if word.lower() == user_input_lower
    ]
    try:
        return worksheets_names[0]
    except IndexError:
        raise WorksheetNotFoundError


def get_all_worksheets_indexed_titles() -> dict:
    """
    Function that returns worksheet titles and indexes in a form of dictionary
    """
    worksheets = SHEET.worksheets()
    indexed_titles = {}
    for worksheet in worksheets:
        indexed_titles[worksheet.title] = [worksheet.index]
    return indexed_titles


def sheet_new_index(validated_input: str) -> int:
    """
    Function that returns new index for duplicated sheet.
    It makes that new copy will always appear to the right of worksheets tab
    Indexes of rest of worksheets will be incremented accordingly
    """
    old_index = get_sheet_index(validated_input)
    new_index = old_index + 1
    return new_index


def get_sheet_index(validated_input: str) -> int:
    """
    Function that should take the output of validate_user_chosen_sheet function
    and return the index of correct worksheet
    """
    index = get_all_worksheets_indexed_titles()[validated_input][0]
    return index


def delete_worksheet():
    """
    Function that delete worksheet from a spreadsheet
    """
    user_input = input("Enter the worksheet name to delete: ")
    try:
        worksheet_name = validate_user_chosen_sheet(user_input)
    except WorksheetNotFoundError:
        print("Worksheet not found")
        return
    if (
        len(get_all_worksheets_titles()) > 1
        and not worksheet_name == get_all_worksheets_titles()[0]
    ):
        print("Processing ...")
        sheet_to_remove = SHEET.worksheet(worksheet_name)
        SHEET.del_worksheet(sheet_to_remove)
        print("Sheet successfully removed !")
    elif worksheet_name == get_all_worksheets_titles()[0]:
        print("You can't delete template worksheet")

    elif len(get_all_worksheets_titles()) == 1:
        print("You can't delete all the sheets in a spreadsheet.")

    else:
        print("Could not remove worksheet")


def add_worksheet():
    """
    Function that adds a worksheet to a spreadsheet
    """
    user_input = input("Enter the name of the new worksheet: ")
    if check_if_worksheet_exist(user_input) == False:
        print("Processing...")
        sheet_title = user_input
        SHEET.add_worksheet(title=sheet_title, rows=200, cols=6)
        print("SHEET successfully added !")
    else:
        print("You cant add the sheet with the same name")


def duplicate_sheet():
    """
    Function that duplicates chosen sheet
    """
    user_input = input("Enter the name of the sheet to copy: ")
    try:
        worksheet_name = validate_user_chosen_sheet(user_input)
        print("Processing ...")
        sheet_id = get_all_worksheets_titles_with_id()[worksheet_name][0]
        sheet_index = sheet_new_index(worksheet_name)
        SHEET.duplicate_sheet(source_sheet_id=sheet_id, insert_sheet_index=sheet_index)
        print("Worksheet successfully duplicated !")
    except WorksheetNotFoundError:
        print("Worksheet not found")
        return


def rename_sheet():
    """
    Function that renames the chosen worksheet by the user.
    """
    user_input = input("Enter the worksheet name to rename: ")
    try:
        validated_input = validate_user_chosen_sheet(user_input)
        user_input_new_name = input("Enter new worksheet name: ")
        if (
            not check_if_worksheet_exist(user_input_new_name)
            and len(user_input_new_name) > 0
            and not validated_input == get_all_worksheets_titles()[0]
        ):
            print("Processing ...")
            index = get_sheet_index(validated_input)
            sheet_to_rename = SHEET.get_worksheet(index)
            sheet_to_rename.update_title(user_input_new_name)
            print("Worksheet successfully renamed !")
        elif len(user_input_new_name) <= 0:
            print("A worksheet name must be at least 1 character long !")
            return
        elif (
            not check_if_worksheet_exist(user_input_new_name)
            and len(user_input_new_name) > 0
            and validated_input == get_all_worksheets_titles()[0]
        ):
            print("You can't rename the template worksheet")
        else:
            print(f"Worksheet with name {validated_input} already exist !")
    except WorksheetNotFoundError:
        print("Worksheet not found")
        return


def set_active_worksheet():
    """
    Function that will change the active worksheet
    """
    global current_worksheet
    print_all_worksheets()
    try:
        user_input = input("Enter the worksheet name that you will work on: ")
        validated_input = validate_user_chosen_sheet(user_input)
    except WorksheetNotFoundError:
        print("Worksheet not found")
        return
    if validated_input == get_all_worksheets_titles()[0]:
        print("You cant work on the the template worksheet")

    else:
        current_worksheet = validated_input
        return current_worksheet


def check_active_worksheet():
    """
    Funtion that checks if active worksheet was selected
    """
    global current_worksheet
    if current_worksheet == None:
        return False
    else:
        return True


def print_worksheet_content():
    """
    Function that prints current worksheet content
    """
    global current_worksheet
    if not check_active_worksheet():
        print("No active worksheet was selected.")
    else:
        my_worksheet = SHEET.worksheet(current_worksheet)
        data = my_worksheet.get_all_values()
        data_to_print = tabulate(
            data, headers="firstrow", numalign="center", stralign="center"
        )
        print(data_to_print)


def get_current_keys():
    """
    Function that returns data sorting keys
    """
    global current_worksheet
    try:
        if not check_active_worksheet():
            print("No active worksheet was selected.")
        else:
            active_worksheet = current_worksheet
            selected_worksheet = SHEET.worksheet(active_worksheet)
            all_data = selected_worksheet.get_all_values()
            keys = []
            for item in all_data[0]:
                keys.append(item)
            return keys
    except IndexError:
        keys = []
        return keys


def check_keys_for_duplicates(keys_candidate) -> bool:
    """
    Functions that will check if data sorting keys are unique
    """
    compare_keys = []
    for key in keys_candidate:
        compare_keys.append(key.lower())

    if len(compare_keys) == len(set(compare_keys)) and len(compare_keys) >= 1:
        return True
    else:
        return False

def clear_worksheet():
    """
    Function that removes clears the worksheet from all values
    """
    global current_worksheet
    if not check_active_worksheet():
        print("No active worksheet was selected.")
    else:
        my_worksheet = SHEET.worksheet(current_worksheet)
        print('Processing ...')
        my_worksheet.clear()
        print('The worksheet was successfully cleared')
        print('Remember to set new data sorting keys, before moving on !')

