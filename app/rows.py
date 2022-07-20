import gspread
import pandas as pd

from app import app_config as config
from app import keys, messages, validation, worksheet


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
    updated_keys_len = len(keys.remove_empty_string_from_keys(current_keys))
    last_row_of_data = get_last_row_number()
    if updated_keys_len == 0:
        print("Set your data sorting keys first !")
        return new_row
    elif last_row_of_data > 200:
        print(
            "You can't add more data. Please, modify the data accordingly or"
            " make another worksheet"
        )
        return new_row
    else:
        print(f"You will add the data to row: {last_row_of_data}")
        for i in range(1, updated_keys_len + 1):
            new_cell_value = input(
                f"Enter value for cell {i} in row {last_row_of_data}:\n"
            )
            new_cell_value = worksheet.replace_space_with_underscore(
                new_cell_value
            )
            new_row.append(new_cell_value)
        return new_row


def append_rows(user_row_candidate: list, row_number: int) -> None:
    """
    Function that append data to the next row in the worksheet
    """
    try:
        current_worksheet = config.SHEET.worksheet(config.current_worksheet)
        last_row_of_data = get_last_row_number()
    except gspread.exceptions.WorksheetNotFound:
        return
    if len(keys.get_current_keys()) == 0:
        return
    elif last_row_of_data > 200:
        return
    prompt_user = messages.user_confirmation()
    if prompt_user:
        print("Processing ...")
        current_worksheet.append_row(
            user_row_candidate, table_range=f"A{row_number}"
        )
        print("Data added successfully !")
    else:
        print("Operation cancelled")


def get_user_data_range() -> tuple:
    """
    Function that get the range of records to display in the table
    """
    while True:
        try:
            start_number = int(
                input("Enter the starting number from 1 to 200:\n")
            )
            end_number = int(
                input("Enter the end number from from 1 to 200:\n")
            )
        except ValueError:
            print("Not a number")
            continue
        if (
            start_number <= 0 or
            end_number <= 0 or
            start_number > 200 or
            end_number > 200
        ):
            print("Invalid range")
            continue
        return start_number - 1, end_number


def calculate_row_range(user_input: int, row_len: int) -> list:
    """
    Function that calculates the required amount of indexes and returns them
    in the list. Return format example: ['R1', 'R2']
    """
    row_counter = []
    for i in range(1, row_len + 1):
        i = i + 1
        row_counter.append(f"R{i + user_input -1}")
    return row_counter


def calculate_column_range(column_len: int) -> list:
    """
    Function that calculates the required amount of columns and returns them
    Return format example: ['C1', 'C2']
    """
    column_counter = []
    for i in range(column_len):
        i = i + 1
        column_counter.append(f"C{i}")
    return column_counter


def indexed_table() -> None:
    """
    Function that prints current worksheet content, with columns and rows
    symbols in a desired range
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
    if data_indexed.empty:
        print(
            f"Your table is empty in range {start_data_index+1} to"
            f" {end_data_index}"
        )
    else:
        print(data_indexed)


def get_user_cell_to_update() -> tuple:
    """
    Function that ask user for a coordinates of the cell he wants to update
    """
    print(
        "If you want to change the data sorting keys, use the add data sorting"
        " keys from the menu"
    )
    while True:
        try:
            row_number = int(input("Enter the row number from 2 to 200:\n"))
            column_number = int(
                input("Enter the column number from from 1 to 6:\n")
            )
        except ValueError:
            print("Not a number")
            continue
        if (
            row_number < 2 or
            column_number <= 0 or
            row_number > 200 or
            column_number > 6
        ):
            print("Invalid range. Please try again.")
            continue
        return row_number, column_number


def update_cell() -> None:
    """
    Function that update the cell with new value
    """
    if not validation.check_active_worksheet():
        return
    current_keys = keys.get_current_keys()
    if len(current_keys) == 0:
        print("You have to set your data sorting keys first")
        return
    row_number, column_number = get_user_cell_to_update()
    user_input = input("Enter value for a cell: \n")
    cell_candidate = worksheet.replace_space_with_underscore(user_input)
    print("Processing ...")
    print(
        f"Cell with row number {row_number} in column {column_number} will be"
        f" updated with {cell_candidate} value"
    )
    user_confirmation = messages.user_confirmation()
    if user_confirmation:
        worksheet_to_update = config.SHEET.worksheet(config.current_worksheet)
        worksheet_to_update.update_cell(
            row_number, column_number, cell_candidate
        )
        print("Cell was successfully updated!")
    else:
        print("Operation aborted")


def get_user_row_to_update() -> int:
    """
    Function that ask user for a coordinates of the cell he wants to update
    """
    print(
        "If you want to change the data sorting keys, use the add data sorting"
        " keys from the menu"
    )
    while True:
        try:
            row_number = int(input("Enter the row number from 2 to 200:\n"))
        except ValueError:
            print("Not a number")
            continue
        if row_number < 2 or row_number > 200:
            print("Invalid range. Please try again.")
            continue
        return row_number


def get_user_value_for_each_cell() -> list:
    """
    Function that returns list of values for new row
    """
    new_row_value = []
    keys_number = keys.get_current_keys()
    updated_keys_len = len(keys.remove_empty_string_from_keys(keys_number))
    for cell_idx in range(1, updated_keys_len + 1):
        cell_value = input(f"Enter value for cell value {cell_idx}:\n")
        cell_value = worksheet.replace_space_with_underscore(cell_value)
        new_row_value.append(cell_value)
    return new_row_value


def update_row() -> None:
    """
    Function that update row with new values
    """
    if not validation.check_active_worksheet():
        return
    current_keys = keys.get_current_keys()
    if len(current_keys) == 0:
        print("You have to set your data sorting keys first")
        return
    print(len(current_keys))
    row_number = get_user_row_to_update()
    user_values = get_user_value_for_each_cell()
    user_values_formatted = ", ".join(user_values)
    print("Processing ...")
    print(
        f"Row {row_number} will be updated with {user_values_formatted} values"
    )
    user_confirmation = messages.user_confirmation()
    if user_confirmation:
        current_worksheet = config.SHEET.worksheet(config.current_worksheet)
        current_worksheet.batch_update(
            [
                {
                    "range": f"A{row_number}:F{row_number}",
                    "values": [user_values],
                },
            ]
        )
        print("Row was successfully updated !")
    else:
        print("Operation aborted")
