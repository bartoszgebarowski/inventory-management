import time


def print_menu():
    "Function that will print out the main menu"
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


def wait_in_seconds(time_to_wait: int):
    """
    Function that will pause the program for desired number of seconds
    """
    time.sleep(time_to_wait)


def help():
    # TODO description of all operations
    """
    Function that will print out the
    """
    print("HELP MENU")
    input("Press any key to leave the help submenu:\n")


def user_confirmation() -> bool:
    """
    Function that will prompt the user for confirming the action
    """
    user_input = input(
        "Are you sure ? Press y to confirm, or any other key to cancel the operation:\n"
    )
    user_input_lower = user_input.lower()
    if user_input_lower == "y":
        return True
    else:
        return False
