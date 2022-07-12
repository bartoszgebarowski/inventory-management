from app import worksheet, messages


while True:
    messages.print_menu()
    user_input = input("Make your selection:\n")
    user_choice_lower = user_input.lower()
    if user_choice_lower == "1":
        worksheet.print_all_worksheets()
        worksheet.set_active_worksheet()
        messages.wait_in_seconds(2)
    elif user_choice_lower == "2":
        worksheet.print_all_worksheets()
        worksheet.add_worksheet()
        messages.wait_in_seconds(2)
    elif user_choice_lower == "3":
        worksheet.print_all_worksheets()
        worksheet.rename_sheet()
        messages.wait_in_seconds(2)
    elif user_choice_lower == "4":
        worksheet.print_all_worksheets()
        worksheet.delete_worksheet()
        messages.wait_in_seconds(2)
    elif user_choice_lower == "5":
        worksheet.print_all_worksheets()
        worksheet.duplicate_sheet()
        messages.wait_in_seconds(2)
    elif user_choice_lower == "6":
        worksheet.print_worksheet_content()
        messages.wait_in_seconds(2)
    elif user_choice_lower == "7":
        worksheet.clear_worksheet()
        messages.wait_in_seconds(2)
    elif user_choice_lower == "h" or user_choice_lower == "help":
        messages.help()
    elif user_choice_lower == "q":
        print("Exit the program. Thanks for using Inventory Management !")
        break
    else:
        print("Input not recognized. Please try again.")
        messages.wait_in_seconds(2)
