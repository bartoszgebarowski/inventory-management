from app import worksheet, validation, config
current_worksheet = 'Copy of Stock'

def get_user_keys() -> list:
    """
    Function that returns keys chosen by user
    """
    print_keys()
    chosen_keys = []
    desired_range = choose_number_of_keys()
    if desired_range:
        for i in range(1, desired_range + 1):
            chosen_keys.append(input(f"Enter key number {i}: "))
    return chosen_keys


def get_current_keys() -> list:
    """
    Function that returns data sorting keys
    """
    global current_worksheet
    keys = []
    
    if not validation.check_active_worksheet():
        print("No active worksheet was selected.")
        return keys
    else:
        active_worksheet = current_worksheet
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
    global current_worksheet
    if not validation.check_active_worksheet():
        print("No active worksheet was selected.")
    elif validation.check_active_worksheet() and not validation.check_keys_for_duplicates(get_current_keys()):
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
    current_keys = get_current_keys()
    if validation.check_keys_for_duplicates(current_keys) == False:
        print("You haven't set your data sorting keys")
        return 0
    if user_input_number_of_keys > len(current_keys):
        print("You have chosen more keys than you currently have")
        return 0
    # TODO: change to raise custom error if number is incorrect
    return int(user_input_number_of_keys)

def filter_data_by_keys(value_split):
    """
    Function that will filter out the data by the chosen keys
    """
    global current_worksheet
    user_keys = validation.validate_user_keys(get_user_keys())

    worksheet = config.SHEET.worksheet(current_worksheet)
    data = worksheet.get_all_records()
    store = []
    for item in data:
        for key in user_keys:
            store.append(item[key])
    stringified = [str(int_) for int_ in store]
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

def update_multiple_sorting_keys():
    """
    Function that updates existing data sorting keys
    """
    global current_worksheet
    worksheet = config.SHEET.worksheet(current_worksheet)
    user_keys = get_user_new_keys()
    validated_keys = validation.check_input_if_first_char_is_space(user_keys)
    duplication_validation = validation.check_keys_for_duplicates(user_keys)
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
            input("Enter how many keys do you want to add/update: ")
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
    if keys_number > 6:
        print("'You cant add more than 6 keys'")
    elif keys_number == 0:
        print('No data')
    else:
        for i in range(1, keys_number + 1):
            new_keys.append(input(f"Enter key number {i}: "))
    return new_keys

def set_new_keys():
    """
    Function that set new data sorting keys if none are present in the worksheet
    """
    global current_worksheet
    worksheet = config.SHEET.worksheet(current_worksheet)
    values_list = worksheet.row_values(1)
    validated_keys = input_new_keys(get_number_of_new_keys())
    evaluated_list = validation.check_input_if_first_char_is_space(validated_keys)
    duplicate_check = validation.check_keys_for_duplicates(evaluated_list)
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
