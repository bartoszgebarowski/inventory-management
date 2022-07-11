from app import worksheet


while True:
    worksheet.print_menu()
    user_input = input('User choice:\n')
    user_choice_lower = user_input.lower()
    if user_choice_lower == 'a':
        worksheet.print_all_worksheets()
        worksheet.add_worksheet()
    elif user_choice_lower == 'r':
        worksheet.print_all_worksheets()
        worksheet.rename_sheet()
    elif user_choice_lower == 's':
        worksheet.print_all_worksheets()
        worksheet.set_active_worksheet()
    elif user_choice_lower == 'del':
        worksheet.print_all_worksheets()
        worksheet.delete_worksheet()
    elif user_choice_lower == 'dup':
        worksheet.print_all_worksheets()
        worksheet.duplicate_sheet()
    elif user_choice_lower == 'pc':
        worksheet.print_worksheet_content()
    elif user_choice_lower == 'cw':
        worksheet.clear_worksheet()
    elif user_choice_lower == 'q':
        print('Exit the program. Thanks for using Inventory Management !')
        break
    else:
        print('Invalid input')
