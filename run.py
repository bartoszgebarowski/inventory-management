import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate
import pandas as pd

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


def get_current_keys() -> list:
    """
    Function that returns data sorting keys
    """
    global current_worksheet
    keys = []
    try:
        if not check_active_worksheet():
            print("No active worksheet was selected.")
            return keys
        else:
            active_worksheet = current_worksheet
            selected_worksheet = SHEET.worksheet(active_worksheet)
            all_data = selected_worksheet.get_all_values()
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
        print("Processing ...")
        my_worksheet.clear()
        print("The worksheet was successfully cleared")
        print("Remember to set new data sorting keys, before moving on !")


def print_keys():
    """
    Function that will print out the data sorting keys
    """
    global current_worksheet
    if not check_active_worksheet():
        print("No active worksheet was selected.")
    elif check_active_worksheet() and not check_keys_for_duplicates(get_current_keys()):
        print("You have to set your data sorting keys first !")
    else:
        keys = get_current_keys()
        data_to_print = " ".join(keys)
        print(f"Data sorting keys: {data_to_print}")


def choose_number_of_keys() -> int:
    """
    Function that will return the number of keys that the user want to use for data filtering
    """
    try:
        user_input_number_of_keys = int(
            input("Enter how many keys do you want to use: ")
        )
    except ValueError:
        print("Your input must be integer")
        return 0
    if user_input_number_of_keys == 0:
        print("Zero cant be chosen")
        return 0
    elif check_keys_for_duplicates(get_current_keys()) == False:
        print("You haven't set your data sorting keys")
        return 0
    elif user_input_number_of_keys > len(get_current_keys()):
        print("You have chosen more keys than you currently have")
        return 0
    else:
        return int(user_input_number_of_keys)


def get_user_keys() -> list:
    """
    Function that returns keys chosen by user
    """
    print_keys()
    chosen_keys = []
    desired_range = choose_number_of_keys()
    if desired_range > 0:
        for i in range(1, desired_range + 1):
            chosen_keys.append(input(f"Enter key number {i}: "))
    return chosen_keys


def validate_user_keys(keys_candidate) -> list:
    """
    Function that validates user keys
    """
    user_keys = keys_candidate
    worksheet_keys = get_current_keys()
    validated_keys = [
        b for b in worksheet_keys if b.lower() in (a.lower() for a in user_keys)
    ]
    result = any(elem in validated_keys for elem in worksheet_keys)
    if result:
        return validated_keys
    else:
        print("Keys do not match")
        validated_keys = []
        return validated_keys


def filter_data_by_keys(value_split):
    """
    Function that will filter out the data by the chosen keys
    """
    global current_worksheet
    user_keys = validate_user_keys(get_user_keys())

    worksheet = SHEET.worksheet(current_worksheet)
    data = worksheet.get_all_records()
    store = []
    for item in data:
        for key in user_keys:
            store.append(item[key])
    stringified = [str(int) for int in store]
    data_to_print = "\n".join(
        [
            " | ".join(stringified[i : i + value_split])
            for i in range(0, len(stringified), value_split)
        ]
    )
    print(data_to_print)


def get_user_new_keys() -> list:
    """
    Function that returns a list of keys, in range of existing keys
    """
    current_keys = get_current_keys()
    current_keys_len = len(current_keys)

    new_keys = []
    for i in range(1, current_keys_len + 1):
        new_keys.append(input(f"Enter key number {i}: "))
    return new_keys


def check_input_if_first_char_is_space(new_keys_candidate) -> list:
    """
    Function that check if first character in item is a space and returns a list without items, that are starting with space
    """
    try:
        evaluated_list = [item for item in new_keys_candidate if item[0] != " "]
    except IndexError:
        evaluated_list = []
        return evaluated_list
    else:
        return evaluated_list


def update_multiple_sorting_keys():
    """
    Function that updates existing data sorting keys
    """
    global current_worksheet
    worksheet = SHEET.worksheet(current_worksheet)
    user_keys = get_user_new_keys()
    validated_keys = check_input_if_first_char_is_space(user_keys)
    duplication_validation = check_keys_for_duplicates(user_keys)
    if len(validated_keys) != len(user_keys):
        print("Invalid input")
    elif not duplication_validation:
        print("Keys are not unique")
    else:
        print("Processing ...")
        worksheet.batch_update(
            [
                {"range": "A1:F1", "values": [user_keys]},
            ]
        )
        print("Keys were updated successfully")


def get_number_of_new_keys() -> int:
    """
    Function that returns a number of keys that user want to create
    """
    try:
        user_input_number_of_keys = int(
            input("Enter how many keys do you want to use: ")
        )
    except ValueError:
        print("Your input must be integer")
        return 0
    if user_input_number_of_keys == 0:
        print("Zero cant be chosen")
        return 0
    else:
        return int(user_input_number_of_keys)


def input_new_keys(keys_number) -> list:
    """
    Function that retuns list of inputs
    """
    new_keys = []
    if keys_number == 0:
        print("No data")
        new_keys = []
        return new_keys
    else:
        for i in range(1, keys_number + 1):
            new_keys.append(input(f"Enter key number {i}: "))
    return new_keys


def set_new_keys():
    """
    Function that set new data sorting keys if none are present in the worksheet
    """
    global current_worksheet
    worksheet = SHEET.worksheet(current_worksheet)
    values_list = worksheet.row_values(1)
    validated_keys = input_new_keys(get_number_of_new_keys())
    evaluated_list = check_input_if_first_char_is_space(validated_keys)
    duplicate_check = check_keys_for_duplicates(evaluated_list)
    if len(values_list) >= 1:
        print("You already have the keys.")
    elif len(validated_keys) == 0:
        print("Invalid data")
    elif len(evaluated_list) != len(validated_keys):
        print("Space as a first character is not allowed")
    elif not duplicate_check:
        print("Your keys are not unique")
    else:
        print("Processing ...")
        worksheet.batch_update(
            [
                {"range": "A1:F1", "values": [validated_keys]},
            ]
        )
        print("Keys were set successfully")


def get_user_data_range() -> list:
    """
    Function that get the range of records to display in the table
    """
    numbers_to_display = []
    try:
        start_number = int(input("Enter the starting number from 1 to 200: "))
        end_number = int(input("Enter the end number from from 1 to 200: "))
    except ValueError:
        print("Not a number")
        return numbers_to_display
    else:
        if start_number <= 0 or start_number > 200:
            print("Invalid range")
            return numbers_to_display
        elif end_number <= 0 or end_number > 200:
            print("Invalid range")
            return numbers_to_display
        else:
            numbers_to_display.append(start_number)
            numbers_to_display.append(end_number)
            return numbers_to_display


def calculate_row_range(row_range: list) -> list:
    """
    Function that calculates the required amount of indexes and returns them in the list
    """
    row_counter = []
    for i in range(len(row_range)):
        i = i + 1
        row_counter.append(f"R{i}")
    return row_counter


def calculate_column_range(column_range: list) -> list:
    """
    Function that calculates the required amount of columns and returns them in the list
    """
    column_counter = []
    for i in range(len(column_range)):
        i = i + 1
        column_counter.append(f"C{i}")
    return column_counter


def indexed_table(user_range):
    """
    Function that prints current worksheet content, with columns and rows symbols in a desired range
    """
    global current_worksheet
    if not check_active_worksheet():
        print("No active worksheet was selected.")
    elif len(user_range) == 0:
        print("No range available")
    else:
        my_worksheet = SHEET.worksheet(current_worksheet)
        data = my_worksheet.get_all_values()[user_range[0] - 1 : user_range[1] + 1]
        row_counter = calculate_row_range(data)
        column_counter = calculate_column_range(get_current_keys())
        pd.set_option("display.max_rows", 200)
        data_indexed = pd.DataFrame(
            data, index=pd.Index(row_counter), columns=pd.Index(column_counter)
        )
        print(data_indexed)
