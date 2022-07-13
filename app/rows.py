from app import keys, worksheet, messages
import gspread
from app import app_config as config


def get_user_data_range() -> list:
    """
    Function that get the range of records to display in the table
    """
    numbers_to_display = []
    try:
        start_number = int(input("Enter the starting number from 1 to 200:\n"))
        end_number = int(input("Enter the end number from from 1 to 200:\n"))
    except ValueError:
        print("Not a number")
        return numbers_to_display

    if start_number <= 0 or start_number > 200:
        print("Invalid range")

    elif end_number <= 0 or end_number > 200:
        print("Invalid range")

    else:
        numbers_to_display.append(start_number)
        numbers_to_display.append(end_number)
    return numbers_to_display


def calculate_row_range(user_input: int, row_len: int) -> list:
    """
    Function that calculates the required amount of indexes and returns them in the list
    """
    row_counter = []
    for i in range(row_len):
        i = i + 1
        row_counter.append(f"R{i + user_input -1}")
    return row_counter


def calculate_column_range(column_len: int) -> list:
    """
    Function that calculates the required amount of columns and returns them in the list
    """
    column_counter = []
    for i in range(column_len):
        i = i + 1
        column_counter.append(f"C{i}")
    return column_counter


def get_last_row_number() -> int:
    """
    Function that returns last row
    """
    try:
        current_worksheet = config.SHEET.worksheet(config.current_worksheet)
    except gspread.exceptions.WorksheetNotFound:
        return 0
    else:
        worksheet_all_values_length = len(current_worksheet.get_all_values())
        return worksheet_all_values_length + 1


def get_user_new_row() -> list:
    """
    Function that returns a list of keys, in range of existing keys
    """
    new_row = []
    try:
        config.SHEET.worksheet(config.current_worksheet)
    except gspread.exceptions.WorksheetNotFound:
        print("No worksheet was set")
        return new_row
    current_keys = keys.get_current_keys()
    current_keys_length = len(current_keys)
    last_row_of_data = get_last_row_number()
    if current_keys_length == 0:
        print("Set your data sorting keys first !")
        return new_row
    elif last_row_of_data > 200:
        print(
            "You can't add more data. Please, modify the data accordingly or make another worksheet"
        )
        return new_row
    else:
        print(f"You will add the data to row: {last_row_of_data}")
        for i in range(1, current_keys_length + 1):
            new_cell_value = input(
                f"Enter value for cell {i} in row {last_row_of_data}:\n"
            )
            new_cell_value = worksheet.replace_space_with_underscore(new_cell_value)
            new_row.append(new_cell_value)
        return new_row


def append_rows(user_row_candidate, row_number):
    try:
        current_worksheet = config.SHEET.worksheet(config.current_worksheet)
    except gspread.exceptions.WorksheetNotFound:
        return
    else:
        prompt_user = messages.user_confirmation()
        if prompt_user:
            print("Processing ...")
            current_worksheet.append_row(
                user_row_candidate, table_range=f"A{row_number}"
            )
            print("Data added successfully !")
        else:
            print("Operation cancelled")
