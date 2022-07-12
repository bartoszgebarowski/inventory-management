from app.errors import WorksheetNotFoundError
from app import app_config as config
from app import worksheet, keys


def validate_user_chosen_sheet(input_candidate: str, worksheets_to_check: list) -> str:
    """
    Function that checks if user input exist as a worksheet
    """
    user_input_lower = input_candidate.lower()
    worksheets_names = [
        worksheet for worksheet in worksheets_to_check if worksheet.lower() == user_input_lower
    ]
    try:
        return worksheets_names[0]
    except IndexError:
        raise WorksheetNotFoundError


def check_if_worksheet_exist(input_candidate) -> bool:
    """
    Function that checks if worksheet exist
    """
    user_input_lower = input_candidate.lower()
    worksheets_to_check = worksheet.get_all_worksheets_titles()
    worksheets_names = [
        worksheet for worksheet in worksheets_to_check if worksheet.lower() == user_input_lower
    ]
    return bool(worksheets_names)


def check_active_worksheet():
    """
    Function that checks if active worksheet was selected
    """
    if config.current_worksheet is None:
        return False
    else:
        return True


def check_keys_for_duplicates(keys_candidate: list) -> bool:
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


def validate_user_keys(keys_candidate) -> list:
    """
    Function that validates user keys
    """
    user_keys = keys_candidate
    worksheet_keys = keys.get_current_keys()
    keys_lower = (a.lower() for a in user_keys)
    validated_keys = [b for b in worksheet_keys if b.lower() in keys_lower]
    result = any(elem in validated_keys for elem in worksheet_keys)
    if result:
        return validated_keys
    else:
        print("Keys do not match")
        validated_keys = []
        return validated_keys


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
