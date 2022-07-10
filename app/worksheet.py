from app import config, validation, keys, worksheet
from app.errors import WorksheetNotFoundError
from tabulate import tabulate
import pandas as pd

def get_all_worksheets_titles() -> list:
    """
    Function that returns the list of all worksheets titles
    """
    worksheet_list = config.SHEET.worksheets()
    worksheets_all = []
    for index in range(len(worksheet_list)):
        worksheets_all.append(worksheet_list[index].title)
    return worksheets_all

def get_all_worksheets_titles_with_id() -> dict:
    """
    Function that returns the list of all worksheets titles
    """
    worksheets = config.SHEET.worksheets()
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

def get_all_worksheets_indexed_titles() -> dict:
    """
    Function that returns worksheet titles and indexes in a form of dictionary
    """
    worksheets = config.SHEET.worksheets()
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

def add_worksheet():
    """
    Function that adds a worksheet to a spreadsheet
    """
    user_input = input("Enter the name of the new worksheet: ")
    if validation.check_if_worksheet_exist(user_input) == False:
        print("Processing...")
        sheet_title = user_input
        config.SHEET.add_worksheet(title=sheet_title, rows=200, cols=6)
        print("SHEET successfully added !")
    else:
        print("You cant add the sheet with the same name")

def delete_worksheet():
    """
    Function that delete worksheet from a spreadsheet
    """
    user_input = input("Enter the worksheet name to delete: ")
    words_to_check = get_all_worksheets_titles()
    try:
        worksheet_name = validation.validate_user_chosen_sheet(user_input, words_to_check)
    except WorksheetNotFoundError:
        print("Worksheet not found")
        return
    if (
        len(get_all_worksheets_titles()) > 1
        and not worksheet_name == get_all_worksheets_titles()[0]
    ):
        print("Processing ...")
        sheet_to_remove = config.SHEET.worksheet(worksheet_name)
        config.SHEET.del_worksheet(sheet_to_remove)
        print("Sheet successfully removed !")
    elif worksheet_name == get_all_worksheets_titles()[0]:
        print("You can't delete template worksheet")

    elif len(get_all_worksheets_titles()) == 1:
        print("You can't delete all the sheets in a spreadsheet.")

    else:
        print("Could not remove worksheet")

def set_active_worksheet():
    """
    Function that will change the active worksheet
    """
    global current_worksheet
    print_all_worksheets()
    try:
        user_input = input("Enter the worksheet name that you will work on: ")
        words_to_check = get_all_worksheets_titles()
        validated_input = validation.validate_user_chosen_sheet(user_input, words_to_check)
    except WorksheetNotFoundError:
        print("Worksheet not found")
        return
    if validated_input == get_all_worksheets_titles()[0]:
        print("You cant work on the the template worksheet")

    else:
        current_worksheet = validated_input
        return current_worksheet

def duplicate_sheet():
    """
    Function that duplicates chosen sheet
    """
    user_input = input("Enter the name of the sheet to copy: ")
    words_to_check = get_all_worksheets_titles()
    try:
        worksheet_name = validation.validate_user_chosen_sheet(user_input, words_to_check)
        print("Processing ...")
        sheet_id = get_all_worksheets_titles_with_id()[worksheet_name][0]
        sheet_index = sheet_new_index(worksheet_name)
        config.SHEET.duplicate_sheet(source_sheet_id=sheet_id, insert_sheet_index=sheet_index)
        print("Worksheet successfully duplicated !")
    except WorksheetNotFoundError:
        print("Worksheet not found")
        return

def rename_sheet():
    """
    Function that renames the chosen worksheet by the user.
    """
    user_input = input("Enter the worksheet name to rename: ")
    words_to_check = get_all_worksheets_titles()
    validated_input = validation.validate_user_chosen_sheet(user_input, words_to_check)
    user_input_new_name = input("Enter new worksheet name: ")
    try:
        worksheet_exist = validation.check_if_worksheet_exist(user_input_new_name)
    except WorksheetNotFoundError:
        print("Worksheet not found")
        return
    if (
        not worksheet_exist
        and len(user_input_new_name) > 0
        and not validated_input == get_all_worksheets_titles()[0]
    ):
        print("Processing ...")
        index = get_sheet_index(validated_input)
        sheet_to_rename = config.SHEET.get_worksheet(index)
        sheet_to_rename.update_title(user_input_new_name)
        print("Worksheet successfully renamed !")
    elif len(user_input_new_name) <= 0:
        print("A worksheet name must be at least 1 character long !")
        return
    elif (
        not worksheet_exist
        and len(user_input_new_name) > 0
        and validated_input == get_all_worksheets_titles()[0]
    ):
        print("You can't rename the template worksheet")
    else:
        print(f"Worksheet with name {validated_input} already exist !")

def print_worksheet_content():
    """
    Function that prints current worksheet content
    """
    global current_worksheet
    if not validation.check_active_worksheet():
        print("No active worksheet was selected.")
    else:
        my_worksheet = config.SHEET.worksheet(current_worksheet)
        data = my_worksheet.get_all_values()
        data_to_print = tabulate(
            data, headers="firstrow", numalign="center", stralign="center"
        )
        print(data_to_print)

def clear_worksheet():
    """
    Function that removes clears the worksheet from all values
    """
    global current_worksheet
    if not validation.check_active_worksheet():
        print("No active worksheet was selected.")
    else:
        my_worksheet = config.SHEET.worksheet(current_worksheet)
        print("Processing ...")
        my_worksheet.clear()
        print("The worksheet was successfully cleared")
        print("Remember to set new data sorting keys, before moving on !")

def indexed_table(user_range):
    """
    Function that prints current worksheet content, with columns and rows symbols in a desired range
    """
    global current_worksheet
    if not validation.check_active_worksheet():
        print("No active worksheet was selected.")
    elif len(user_range) == 0:
        print("No range available")
    else:
        my_worksheet = config.SHEET.worksheet(current_worksheet)
        data = my_worksheet.get_all_values()[user_range[0] - 1 : user_range[1]]
        print(data)
        row_counter = keys.calculate_row_range(user_range[0], len(data))
        column_counter = keys.calculate_column_range(len(keys.get_current_keys()))
        pd.set_option("display.max_rows", 200)
        data_indexed = pd.DataFrame(
            data, index=pd.Index(row_counter), columns=pd.Index(column_counter)
        )
        print(data_indexed)