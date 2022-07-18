import gspread.exceptions
from tabulate import tabulate

from app import app_config as config
from app import messages, validation
from app.errors import WorksheetNotFoundError


def get_all_worksheets_titles() -> list:
    """
    Function that returns the list of all worksheets titles
    """
    worksheet_list = config.SHEET.worksheets()
    worksheets_all = []
    for worksheet in worksheet_list:
        worksheets_all.append(worksheet.title)
    return worksheets_all


def get_all_worksheets_titles_with_id() -> dict:
    """
    Function that returns the dictionary of all worksheets titles with id
    """
    worksheets = config.SHEET.worksheets()
    worksheets_titles_with_id = {}
    for worksheet in worksheets:
        worksheets_titles_with_id[worksheet.title] = worksheet.id
    return worksheets_titles_with_id


def print_all_worksheets() -> None:
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
        indexed_titles[worksheet.title] = worksheet.index
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
    index = get_all_worksheets_indexed_titles()[validated_input]
    return index


def add_worksheet() -> None:
    """
    Function that adds a worksheet to a spreadsheet
    """
    user_input = input("Enter the name of the new worksheet:\n")
    if validation.check_if_worksheet_exist(user_input) is False:
        print("Processing...")
        worksheet_title = replace_space_with_underscore(user_input)
        config.SHEET.add_worksheet(title=worksheet_title, rows=200, cols=6)
        print(
            f"Worksheet with the name {worksheet_title} was successfully added"
            " to the spreadsheet!"
        )
    else:
        print("You cant add the sheet with the same name")


def delete_worksheet() -> None:
    """
    Function that delete worksheet from a spreadsheet
    """
    user_input = input("Enter the worksheet name to delete:\n")
    worksheets_to_check = get_all_worksheets_titles()
    try:
        worksheet_name = validation.validate_user_chosen_sheet(
            user_input, worksheets_to_check
        )
    except WorksheetNotFoundError:
        print("Worksheet not found")
        return
    if not messages.user_confirmation():
        print("Operation cancelled")
    elif len(worksheets_to_check) <= 1:
        print("You can't delete all the sheets in a spreadsheet.")
    elif worksheet_name == worksheets_to_check[0]:
        print("You can't delete template worksheet")
    else:
        print("Processing ...")
        sheet_to_remove = config.SHEET.worksheet(worksheet_name)
        config.SHEET.del_worksheet(sheet_to_remove)
        print("Sheet successfully removed !")


def set_active_worksheet() -> None | str:
    """
    Function that will change the active worksheet
    """
    try:
        user_input = input("Enter the worksheet name that you will work on:\n")
        worksheets_to_check = get_all_worksheets_titles()
        validated_input = validation.validate_user_chosen_sheet(
            user_input, worksheets_to_check
        )
    except WorksheetNotFoundError:
        print("Worksheet not found")
        return
    if validated_input == get_all_worksheets_titles()[0]:
        print("You cant work on the the template worksheet")

    else:
        config.current_worksheet = validated_input
        print(f"Current active worksheet: {validated_input}")
        return config.current_worksheet


def duplicate_sheet() -> None:
    """
    Function that duplicates chosen sheet
    """
    user_input = input("Enter the name of the sheet to copy:\n")
    worksheets_to_check = get_all_worksheets_titles()
    try:
        worksheet_name = validation.validate_user_chosen_sheet(
            user_input, worksheets_to_check
        )
        print("Processing ...")
        sheet_id = get_all_worksheets_titles_with_id()[worksheet_name]
        sheet_index = sheet_new_index(worksheet_name)
        config.SHEET.duplicate_sheet(
            source_sheet_id=sheet_id,
            insert_sheet_index=sheet_index,
            new_sheet_name=f"Copy_of_{worksheet_name}",
        )
        print("Worksheet successfully duplicated !")
    except WorksheetNotFoundError:
        print("Worksheet not found")


def rename_sheet() -> None:
    """
    Function that renames the chosen worksheet by the user.
    """
    user_input = input("Enter the worksheet name to rename:\n")
    user_input_new_name = input("Enter new worksheet name:\n")
    try:
        worksheet_exist = validation.check_if_worksheet_exist(
            user_input_new_name
        )
        worksheets_to_check = get_all_worksheets_titles()
        validated_input = validation.validate_user_chosen_sheet(
            user_input, worksheets_to_check
        )
    except WorksheetNotFoundError:
        print("Worksheet not found")
        return
    if (
        not worksheet_exist
        and len(user_input_new_name) > 0
        and not validated_input == worksheets_to_check[0]
    ):
        print("Processing ...")
        index = get_sheet_index(validated_input)
        sheet_to_rename = config.SHEET.get_worksheet(index)
        sheet_to_rename.update_title(user_input_new_name)
        print("Worksheet successfully renamed !")
    elif len(user_input_new_name) <= 0:
        print("A worksheet name must be at least 1 character long !")
    elif (
        not worksheet_exist
        and len(user_input_new_name) > 0
        and validated_input == get_all_worksheets_titles()[0]
    ):
        print("You can't rename the template worksheet")
    else:
        print(f"Worksheet with name {validated_input} already exist !")


def print_worksheet_content() -> None:
    """
    Function that prints current worksheet content
    """
    try:
        worksheet = config.SHEET.worksheet(config.current_worksheet)
    except gspread.exceptions.WorksheetNotFound:
        print("No active worksheet was selected")
        return
    else:
        worksheet_data = worksheet.get_all_values()
        if len(worksheet_data) == 0:
            print("Can't print empty worksheet")
            print('Set your data sorting keys first!')
        else:
            data_to_print = tabulate(
                worksheet_data,
                headers="firstrow",
                numalign="center",
                stralign="center",
            )
            print(data_to_print)


def clear_worksheet() -> None:
    """
    Function that removes clears the worksheet from all values
    """
    if not validation.check_active_worksheet():
        print("No active worksheet was selected.")
    elif not messages.user_confirmation():
        print("Operation cancelled")
    else:
        worksheet = config.SHEET.worksheet(config.current_worksheet)
        print("Processing ...")
        worksheet.clear()
        print("The worksheet was successfully cleared")
        print("Remember to set new data sorting keys, before moving on !")


def replace_space_with_underscore(string_to_evaluate: str) -> str:
    """
    Function that will replace spaces with underscore
    """
    string_to_return = string_to_evaluate.replace(" ", "_")
    return string_to_return
