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
    print("8. If you need help: press h or type help")
    print("9. Exit the program: type q")


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
