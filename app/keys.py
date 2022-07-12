from app import validation, worksheet
from app import app_config as config
import gspread


def get_current_keys() -> list:
    """
    Function that returns data sorting keys
    """
    keys = []

    if not validation.check_active_worksheet():
        print("No active worksheet was selected.")
        return keys
    else:
        active_worksheet = config.current_worksheet
        selected_worksheet = config.SHEET.worksheet(active_worksheet)
        all_data = selected_worksheet.get_all_values()
        try:
            for item in all_data[0]:
                keys.append(item)
        except IndexError:
            keys = []
        return keys


def print_keys():
    """
    Function that will print out the data sorting keys
    """
    if not validation.check_active_worksheet():
        print("No active worksheet was selected.")
    elif (
        validation.check_active_worksheet()
        and not validation.check_keys_for_duplicates(get_current_keys())
    ):
        print("You have to set your data sorting keys first !")
    else:
        keys = get_current_keys()
        keys_to_print = " ".join(keys)
        print(f"Data sorting keys: {keys_to_print}")


def get_user_new_keys() -> list:
    """
    Function that returns a list of keys, in range of existing keys
    """
    current_keys = get_current_keys()
    current_keys_len = len(current_keys)

    new_keys = []
    for i in range(1, current_keys_len + 1):
        new_keys.append(input(f"Enter key number {i}:\n"))
    return new_keys


# TODO one function/ message identical, mssg 6 to user

def get_number_of_new_keys_to_update() -> int:
    """
    Function that returns a number of keys that user want to update
    """
    while True:
        try:
            keys_number = int(
                input("Enter how many keys do you want to update:\n")
            )
            if keys_number > 7:
                print("'You cant add more than 6 keys'")
            elif keys_number == 0:
                print("No data")
            else:
                return keys_number
        except ValueError:
            print("Your input must be integer")

def get_new_keys(keys_number) -> list:
    """
    Function that retuns list of inputs
    """
    new_keys = []
    while True:
        for i in range(1, keys_number + 1):
            key_name = input(f"Enter key number {i}:\n")
            key_name = worksheet.replace_space_with_underscore(key_name)
            new_keys.append(key_name)
        
        if not validation.check_keys_for_duplicates(new_keys):
            new_keys = []
            print('Keys must be unique')
            continue
        return new_keys

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
    
def add_data_sorting_keys():
    """
    Function that add new single key
    """
    try:
        current_worksheet = config.SHEET.worksheet(config.current_worksheet)
    except gspread.exceptions.WorksheetNotFound:
        print('No worksheet was set')
    else: 
        number_of_keys = get_number_of_new_keys_to_update()
        keys_candidate = get_new_keys(number_of_keys)

        if len(keys_candidate) == 0:
            print("Invalid data")
        elif range == 0:
            "No keys"
        while len(keys_candidate) < 6:
            keys_candidate.append('')
        else:
            print("Processing ...")
            current_worksheet.batch_update(
                [
                    {"range": 'A1:F1', "values": [keys_candidate]},
                ]
                )
            print("New data sorting key/keys was/were successfully added !")

