import gspread

from app import app_config as config
from app import validation, worksheet


def get_current_keys() -> list:
    """
    Function that returns current data sorting keys
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


def print_keys(current_keys: list) -> None:
    """
    Function that will print out the sorting keys
    """
    keys_to_string = " ".join(current_keys)
    print(f"Data sorting keys: {keys_to_string}")


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


def get_number_of_new_keys_to_update() -> int:
    """
    Function that returns a number of keys that user want to update
    """
    while True:
        try:
            keys_number = int(
                input("Enter how many keys do you want to update:\n")
            )
            if keys_number > 6:
                print("You can't add more than 6 keys")
            elif keys_number == 0:
                print("Nothing will be altered !")
            elif keys_number < 0:
                print("Input must be positive number.")
            else:
                return keys_number
        except ValueError:
            print("Your input must be integer.")


def get_new_keys(keys_number: int) -> list:
    """
    Function that returns list of inputs
    It replaces the empty inputs in a format "Empty_key_num"
    """
    while True:
        new_keys = []
        for i in range(1, keys_number + 1):
            key_name = input(f"Enter key number {i}:\n")
            key_name = worksheet.replace_space_with_underscore(key_name)
            new_keys.append(key_name)
        for index, key in enumerate(new_keys):
            if key == "":
                new_keys[index] = f"Empty_key{index+1}"
        if not validation.check_for_duplicates(new_keys):
            print("Keys must be unique")
            continue
        return new_keys


def add_data_sorting_keys() -> None:
    """
    Function that add/update sorting keys
    """
    try:
        current_worksheet = config.SHEET.worksheet(config.current_worksheet)
    except gspread.exceptions.WorksheetNotFound:
        print("No worksheet was set")
    else:
        number_of_keys = get_number_of_new_keys_to_update()
        keys_candidate = get_new_keys(number_of_keys)
        if len(keys_candidate) == 0:
            print("Operation failed !")
        while len(keys_candidate) < 6:
            keys_candidate.append("")
        else:
            print("Processing ...")
            current_worksheet.batch_update(
                [
                    {"range": "A1:F1", "values": [keys_candidate]},
                ]
            )
            print("New data sorting key/keys was/were successfully added !")


def remove_empty_string_from_keys(keys: list) -> list:
    """
    Function that will remove the empty key strings from the list
    """
    keys = [key for key in keys if key != ""]
    return keys
