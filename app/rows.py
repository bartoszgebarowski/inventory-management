from app import keys, worksheet, messages, validation
import gspread
from app import app_config as config
import pandas as pd


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
    """
    Function that append data to the next row in the worksheet
    """
    try:
        current_worksheet = config.SHEET.worksheet(config.current_worksheet)
    except gspread.exceptions.WorksheetNotFound:
        return
    prompt_user = messages.user_confirmation()
    if prompt_user:
        print("Processing ...")
        current_worksheet.append_row(user_row_candidate, table_range=f"A{row_number}")
        print("Data added successfully !")
    else:
        print("Operation cancelled")


def get_user_data_range() -> tuple:
    """
    Function that get the range of records to display in the table
    """
    while True:
        try:
            start_number = int(input("Enter the starting number from 1 to 200:\n"))
            end_number = int(input("Enter the end number from from 1 to 200:\n"))
        except ValueError:
            print("Not a number")
            continue
        if (
            start_number <= 0
            or end_number <= 0
            or start_number > 200
            or end_number > 200
        ):
            print("Invalid range")
            continue
        return start_number - 1, end_number


def calculate_row_range(user_input: int, row_len: int) -> list:
    """
    Function that calculates the required amount of indexes and returns them in the list
    """
    row_counter = []
    for i in range(1, row_len + 1):
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


def indexed_table():
    """
    Function that prints current worksheet content, with columns and rows symbols in a desired range
    """
    start_data_index, end_data_index = get_user_data_range()
    if not validation.check_active_worksheet():
        print("No active worksheet was selected.")
        return
    worksheet = config.SHEET.worksheet(config.current_worksheet)
    actual_worksheet_data = worksheet.get_all_values()
    worksheet_data = actual_worksheet_data[start_data_index:end_data_index]
    row_counter = calculate_row_range(start_data_index, len(worksheet_data))
    column_counter = calculate_column_range(len(keys.get_current_keys()))
    pd.set_option("display.max_rows", 200)
    data_indexed = pd.DataFrame(
        worksheet_data,
        index=pd.Index(row_counter),
        columns=pd.Index(column_counter),
    )
    print(data_indexed)


def get_user_cell_to_update() -> tuple:
    """
    Function that ask user for a coordinates of the cell he wants to update
    """
    print('If you want to change the data sorting keys, use the add data sorting keys from the menu')
    while True:
        try:
            row_number = int(input("Enter the row number from 2 to 200:\n"))
            column_number = int(input("Enter the column number from from 1 to 6:\n"))
        except ValueError:
            print("Not a number")
            continue
        if (
            row_number < 2
            or column_number <= 0
            or row_number > 200
            or column_number > 6
        ):
            print("Invalid range. Please try again.")
            continue
        return row_number, column_number


def update_cell():
    "Function that update the cell with new value"
    if not validation.check_active_worksheet():
        return
    row_number, column_number = get_user_cell_to_update()
    user_input = input("Enter value for a cell: \n")
    print("Processing ...")
    print(
        f"Cell with row number {row_number} in column {column_number} will be updated with {user_input} value"
    )
    user_confirmation = messages.user_confirmation()
    if user_confirmation:
        worksheet = config.SHEET.worksheet(config.current_worksheet)
        worksheet.update_cell(row_number, column_number, user_input)
        print("Cell was successfully updated!")
    else:
        print("Operation aborted")
