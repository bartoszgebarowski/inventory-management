import time


def print_menu() -> None:
    """
    Function that prints out the main menu into the terminal
    """
    print("Main menu")
    print("1. Set worksheet to work on: press 1")
    print("2. Add worksheet: press 2")
    print("3. Rename sheet: press 3")
    print("4. Delete worksheet: press 4")
    print("5. Duplicate worksheet: press 5")
    print("6. Print worksheet content: press 6")
    print("7. Remove all content from worksheet: press 7")
    print("8. Add data sorting keys: press 8")
    print("9. Add row of data to a worksheet: press 9")
    print("10. Modify a single cell in a worksheet: press 10")
    print("11. Modify a single row in a worksheet: press 11")
    print("12. If you need help: press h or type help")
    print("13. Exit the program: type q or quit")


def print_help_menu() -> None:
    """
    Function that prints out the help submenu into the terminal
    """
    print("HELP MENU")
    print("1. Set worksheet help menu: press 1")
    print("2. Add worksheet help menu: press 2")
    print("3. Rename worksheet help menu: press 3")
    print("4. Delete worksheet help menu: press 4")
    print("5. Duplicate worksheet help menu: press 5")
    print("6. Print worksheet content help menu: press 6")
    print("7. Remove all content from worksheet help menu: press 7")
    print("8. Add data sorting keys help menu: press 8")
    print("9. Add row of data to a worksheet help menu: press 9")
    print("10. Modify a single cell in a worksheet help menu: press 10")
    print("11. Modify a single row in a worksheet help menu: press 11")
    print("12. Exit the help menu: type q or quit")


def wait_in_seconds(time_to_wait: int) -> None:
    """
    Function that will pause the program for desired number of seconds
    """
    time.sleep(time_to_wait)


def help() -> None:
    """
    Function that brings out the help submenu.
    """
    while True:
        print_help_menu()
        user_input = input("Make your selection:\n")
        user_choice_lower = user_input.lower()
        if user_choice_lower == "1":
            print_help_set_active_worksheet()
        elif user_choice_lower == "2":
            print_help_set_active_worksheet()
        elif user_choice_lower == "3":
            print_help_rename_worksheet()
        elif user_choice_lower == "4":
            print_help_delete_worksheet()
        elif user_choice_lower == "5":
            print_help_duplicate_worksheet()
        elif user_choice_lower == "6":
            print_help_print_worksheet_content()
        elif user_choice_lower == "7":
            print_help_clear_worksheet()
        elif user_choice_lower == "8":
            print_help_add_data_sorting_keys()
        elif user_choice_lower == "9":
            print_help_add_row()
        elif user_choice_lower == "10":
            print_help_modify_single_cell()
        elif user_choice_lower == "11":
            print_help_modify_single_row()
        elif user_choice_lower == "q" or user_choice_lower == "quit":
            break
        else:
            print("Input not recognized. Please try again.")
            wait_in_seconds(1)


def user_confirmation() -> bool:
    """
    Function that will prompt the user for confirming the action
    """
    user_input = input(
        "Are you sure ? Press y to confirm, or any other key to cancel the"
        " operation:\n"
    )
    user_input_lower = user_input.lower()
    if user_input_lower == "y":
        return True
    else:
        return False


def print_help_set_active_worksheet() -> None:
    """
    Function that prints out the help for setting an active worksheet option
    """
    print(
        "This option allows setting a worksheet that user wants to"
        " work with")
    print(
        "If this option is not chosen, adding, modifying or presenting"
        " data in options"
    )
    print("- add data sorting keys")
    print("- print worksheet content ")
    print("- add row of data")
    print("- modify a single cell in a worksheet")
    print("- modify a single row in a worksheet")
    print("Will not be possible")
    print("Template worksheet cannot be chosen in this step.")
    input("Press any key to leave the submenu:\n")


def print_help_add_worksheet() -> None:
    """
    Function that prints out the help for adding worksheet option
    """
    print(
        "This option allows to add a worksheet to a Inventory"
        " Management spreadsheet."
    )
    print("For a worksheet to be created, its name must be unique.")
    print("Spaces will be replaced with underscore for clarity.")
    print(
        "New worksheet will have 6 columns and 200 rows for user"
        " disposal.")
    input("Press any key to leave the submenu:\n")


def print_help_rename_worksheet() -> None:
    """
    Function that prints out the help for renaming a worksheet option
    """
    print(
        "This option allows to rename a worksheet in a Inventory"
        " Management spreadsheet."
    )
    print("First, the user needs to choose a worksheet to rename.")
    print("Next, the user needs to pick a new name for a worksheet.")
    print("New worksheet name needs to be unique for all worksheets.")
    print("Template worksheet cannot be chosen in this step.")
    input("Press any key to leave the submenu:\n")


def print_help_delete_worksheet() -> None:
    """
    Function that prints out the help for deleting a worksheet option
    """
    print(
        "This option allows to delete a worksheet in a Inventory"
        " Management spreadsheet."
    )
    print("To delete a worksheet, the user must pick the worksheet's" " name.")
    print("Template worksheet cannot be chosen in this step.")
    input("Press any key to leave the submenu:\n")


def print_help_duplicate_worksheet() -> None:
    """
    Function that prints out the help for duplicating a worksheet
    """
    print(
                "This option allows to duplicate a worksheet in a Inventory"
                " Management spreadsheet."
            )
    print(
                "To duplicate a worksheet, the user needs to pick a name of a"
                " worksheet to duplicate."
            )
    print(
                "If successful, a new worksheet with 6 columns, 200 rows and"
                " name Copy_of_worksheet_name will be created"
            )
    print("User can rename it by using rename worksheet option")
    input("Press any key to leave the submenu:\n")


def print_help_print_worksheet_content() -> None:
    """
    Function that prints out the help for printing a worksheet content option
    """
    print("This option prints the worksheet content in a table form.")
    print(
                "The user needs to pick a worksheet they wish to operate on by"
                " choosing Set Active Worksheet first."
            )
    print(
                "Data sorting keys need to be chosen by using Add data sorting"
                " keys option, beforehand"
            )
    input("Press any key to leave the submenu:\n")


def print_help_clear_worksheet() -> None:
    """
    Function that prints out the help for clearing a worksheet option
    """
    print("This option allows to clear a worksheet from all of its" " content")
    print(
                "The user needs to pick a worksheet they wish to operate on by"
                " choosing Set Active Worksheet first."
            )
    print("The user will be asked for confirmation")
    input("Press any key to leave the submenu:\n")


def print_help_add_data_sorting_keys() -> None:
    """
    Function that prints out the help for adding a data sorting keys option
    """
    print("This option allows to add a data sorting keys in a worksheet")
    print(
                "The user needs to pick a worksheet they wish to operate on by"
                " choosing Set Active Worksheet first"
            )
    print(
                "It will add/change the values in a first row of a worksheet"
                " to up maximum 6."
            )
    print("The data sorting keys must be unique")
    input("Press any key to leave the submenu:\n")


def print_help_add_row() -> None:
    """
    Function that prints out the help for adding a row of data option
    """
    print(
                "This option allows to add a row of data to a worksheet in a"
                " fastest way"
            )
    print(
                "The user needs to pick a worksheet they wish to operate on by"
                " choosing Set Active Worksheet first"
            )
    print("It will ask user for value for each data sorting key")
    print(
                "If the user is satisfied with the data he entered, he can"
                " either confirm the operation or abort it."
            )
    print("The data will be added to the last empty row in a worksheet")
    input("Press any key to leave the submenu:\n")


def print_help_modify_single_cell() -> None:
    """
    Function that prints out help for modifying a single cell in a worksheet
    """
    print(
        "This option allows to modifying a single cell value in a"
        " worksheet.")
    print(
                "The user needs to pick a worksheet they wish to operate on by"
                " choosing Set Active Worksheet first"
            )
    print(
                "Data sorting keys need to be chosen by using Add data sorting"
                " keys option, beforehand"
            )
    print(
                "To help the user, the program will ask the user for a range"
                " which he wants to see in the terminal."
            )
    print("Table with row and column markings will be presented to user")
    print(
                "Next, the program asks the user for a coordinates of cell he"
                " wants to modify, and the value"
            )
    print(
                "If the user is satisfied with the data he entered, he can"
                " either confirm the operation or abort it."
            )
    input("Press any key to leave the submenu:\n")


def print_help_modify_single_row() -> None:
    """
    Function that prints out help for modifying a single row in a worksheet
    option
    """
    print("This option allows to modify a whole row in a worksheet")
    print(
                "The user needs to pick a worksheet they wish to operate on by"
                " choosing Set Active Worksheet first"
            )
    print(
                "Data sorting keys need to be chosen by using Add data sorting"
                " keys option, beforehand"
            )
    print(
                "To help the user, the program will ask the user for a range"
                " which he wants to see in the terminal."
            )
    print("Table with row and column markings will be presented to user.")
    print(
                "Next, the program asks the user for value for each data"
                " sorting key."
            )
    print(
                "If the user is satisfied with the data he entered, he can"
                " either confirm the operation or abort it."
            )
    input("Press any key to leave the submenu:\n")
