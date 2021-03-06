from app import worksheet, messages, keys, rows


def run_app():
    """
    Main loop
    """
    while True:
        messages.print_menu()
        user_input = input("Make your selection:\n")
        user_choice_lower = user_input.lower()
        if user_choice_lower == "1":
            worksheet.print_all_worksheets()
            worksheet.set_active_worksheet()
        elif user_choice_lower == "2":
            worksheet.print_all_worksheets()
            worksheet.add_worksheet()
        elif user_choice_lower == "3":
            worksheet.print_all_worksheets()
            worksheet.rename_sheet()
        elif user_choice_lower == "4":
            worksheet.print_all_worksheets()
            worksheet.delete_worksheet()
        elif user_choice_lower == "5":
            worksheet.print_all_worksheets()
            worksheet.duplicate_sheet()
        elif user_choice_lower == "6":
            worksheet.print_worksheet_content()
        elif user_choice_lower == "7":
            worksheet.clear_worksheet()
        elif user_choice_lower == "8":
            keys.add_data_sorting_keys()
        elif user_choice_lower == "9":
            rows.append_row(
                rows.get_user_new_row(), rows.get_last_row_number()
                )
        elif user_choice_lower == "10":
            rows.indexed_table()
            rows.update_cell()
        elif user_choice_lower == "11":
            rows.indexed_table()
            rows.update_row()
        elif user_choice_lower == "h" or user_choice_lower == "help":
            messages.help()
        elif user_choice_lower == "q" or user_choice_lower == "quit":
            print("Thanks for using Inventory Management !")
            break
        else:
            print("Input not recognized. Please try again.")
        messages.wait_in_seconds(2)
