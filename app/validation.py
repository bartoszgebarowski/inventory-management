from app import app_config as config
from app import worksheet
from app.errors import WorksheetNotFoundError


def validate_user_chosen_sheet(
    input_candidate: str, worksheets_to_check: list
) -> str:
    """
    Function that checks if user input exist as a worksheet
    """
    user_input_lower = input_candidate.lower()
    worksheets_names = [
        worksheet
        for worksheet in worksheets_to_check
        if worksheet.lower() == user_input_lower
    ]
    try:
        return worksheets_names[0]
    except IndexError:
        raise WorksheetNotFoundError


def check_if_worksheet_exist(input_candidate: str) -> bool:
    """
    Function that checks if worksheet exist
    """
    user_input_lower = input_candidate.lower()
    worksheets_to_check = worksheet.get_all_worksheets_titles()
    worksheets_names = [
        worksheet
        for worksheet in worksheets_to_check
        if worksheet.lower() == user_input_lower
    ]
    return bool(worksheets_names)


def check_active_worksheet() -> bool:
    """
    Function that checks if active worksheet was selected
    """
    return bool(config.current_worksheet)


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
