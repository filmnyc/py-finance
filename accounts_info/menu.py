import datetime
from os import system
import sys
from .transaction_fuctions import trans_act, select_transaction, transaction_list
from .account_fuctions import (create_account, change_account, account_select,
       account_list)
from .transaction_edit import tedit_menu, edit_one, edit_two, edit_three, edit_four, edit_five
# from applets.applet import transaction_list
from .models import engine, Account, db_session, Transaction
from sqlalchemy import func
import json
import decimal, datetime



def account_menu(items):  
    system('clear')
    items = account_list(items)
    print()
    if items["message_opt"] == 'yes':
        print(items["message"])
        print()
        items.update({"message_opt": "no", "message": " "})
    if items["menu_option"] == 'menu':
        pass
    elif items["menu_option"] == 'select' or \
            items["menu_option"] == 'delete' or \
            items["menu_option"] == 'edit':
        items = account_select(items)
        if items["menu_option"] == 'menu':
            account_menu(items)
        elif items["menu_option"] == 'delete':
            items = change_account(items)
            account_menu(items)
        elif items["menu_option"] == 'edit':
            items = change_account(items)
            account_menu(items)
        elif items["menu_option"] == 'transaction':
            items = transaction_menu(items)
        else:
            if items["message_opt"] == 'yes':
                account_menu(items)
    print('Account menu')
    print()
    if items["account_len"] <= items["alter_list"]:
        pass
    else:
        print(' Move down (d) ')
    if items["alter_list"] > items["list_len"]:
        print(' Move up (u) ')
    else:
        pass
    print(' Select (s) ')
    print(' Create (c)')
    print(' Delete (a)')
    print(' Edit (e)')
    print(' Exit (q)')
    print()
    choice = input('Select: ')
    if choice == 'q':
        print("\nExiting...")
        sys.exit()
    elif choice == 'd':
        if items["alter_list"] >= items["account_len"]:
            items.update({"message_opt": "yes", "message": "Wrong direction"})
            account_menu(items)
        else:
            new_list = items["alter_list"] + items["list_len"]
            items.update({"alter_list": new_list, "data_load": "re-load"})
            account_menu(items)
    elif choice == 'u':
        if items["alter_list"] == items["list_len"]:
            items.update({"message_opt": "yes", "message": "Wrong direction"})
            account_menu(items)
        else:
            new_list = items["alter_list"] - items["list_len"]
            items.update({"alter_list": new_list, "data_load": "re-load"})
            account_menu(items)
    elif choice == 's':
        items.update({"menu_option": "select"})
        account_menu(items)
    elif choice == 'c':
        items.update({"menu_option": "create"})
        the_account = create_account(items)
        if the_account == 'reject':
            items.update({"menu_option": "menu"})
            account_menu(items)
        else:
            items.update({"data_load": "re-load"})
            account_menu(items)
    elif choice == 'a':
        items.update({"menu_option": "delete"})
        account_menu(items)
    elif choice == 'e':
        items.update({"menu_option": "edit"})
        account_menu(items)
    else:
        items.update({"message_opt": "yes", "message": "Enter a correct letter"})
        account_menu(items)



# The menu under listed transaction
def transaction_menu(items):
    system('clear')
    print()
    transaction_json, transaction_num = transaction_list(items)
    if items["message_opt"] == 'yes':
        print()
        print(items["message"])
        items.update({"message_opt": "no"})
    if items["menu_option"] == 'select':
        items = select_transaction(items)
        if items["menu_option"] == 'selected':
            transaction_menu(items)
        elif items["menu_option"] == 'select':
            transaction_menu(items)
        elif items["menu_option"] == 'menu':
            transaction_menu(items)
        # elif items["menu_option"] == 'edit_menu':
        #    transaction_edit(items)
    elif items["menu_option"] == 'selected':
        select_transaction(items)
        transaction_edit(items)
    else:
        pass
    print('\nTransaction Menu\n')
    if items["transaction_len"] > items["alter_list"]:
        print(' Page Up (u)')
    if items["alter_list"] > items["list_len"]:
        print(' Page Down (d)')
    print(' Deposit (a)') 
    print(' Withdraw (w)') 
    print(' Edit/Delete Transaction (e)') 
    print(' Main Menu (m)') 
    print(' Quit (q)')
    print()
    change = str(input("Select: "))
    change = change.lower()
    if change == "u":
        if not items["alter_list"] >= items["transaction_len"]:
            system('clear')
            alter_list = items["alter_list"] + items["list_len"]
            items.update({"data_load": "re-load"})
            items.update({"alter_list": alter_list})
            transaction_menu(items)
        else:
            system('clear')
            items.update({"message_opt": "yes"})
            items.update({"message": "\"Selection out of range\""})
            transaction_menu(items)
    elif change == "d":
        if items["alter_list"] - items["list_len"] > 0:
            system('clear')
            alter_list = items["alter_list"] - items["list_len"]
            items.update({"data_load": "re-load", "alter_list": alter_list})
            transaction_menu(items)
        else:
            system('clear')
            items.update({"message_opt": "yes", "message": "\"Selection out of range\""})
            transaction_menu(items)
    elif change == "e": 
        system('clear')
        items.update({"data_load": "load", "transaction_json": transaction_json, "transaction_num": \
                transaction_num, "menu_option": "select"})
        transaction_menu(items)
    elif change == "a": 
        system('clear')
        items.update({"transaction_json": transaction_json, "transaction_num": \
                transaction_num, "menu_option": "Deposit"})
        new_balance, transaction_len = trans_act(items)
        if new_balance == 're-edit':
            items.update({"menu_option": "menu"})
            transaction_menu(items)
        else:
            items.update({"data_load": "re-load", "menu_option": "menu", \
                    "account_balance": new_balance, "transaction_len": \
                    transaction_len})
            transaction_menu(items)
    elif change == "w": 
        system('clear')
        items.update({"transaction_json": transaction_json, "transaction_num": \
                transaction_num, "menu_option": "Withdraw"})
        new_balance, transaction_len = trans_act(items)
        if new_balance == 're-edit':
            items.update({"menu_option": "menu"})
            transaction_menu(items)
        else:
            items.update({"data_load": "re-load", "menu_option": "menu", "account_balance": \
                    new_balance, "transaction_len": transaction_len})
            transaction_menu(items)
    elif change == "m":
        system('clear')
        list_len = items["list_len"]
        items = {"data_load": "re-load", "alter_list": list_len, "message_opt": "no", \
                "message": ' ', "menu_option": "menu", "list_len": list_len}
        account_menu(items)
    elif change == "q":
        print("\nExiting...")
        sys.exit()
    else:
        system('clear')
        items.update({"message_opt": "yes", "message": "\"Invalid input\""})
        print(items["message"])
        transaction_menu(items)


# Edit transaction menu
def transaction_edit(items):
    system('clear')
    transaction_list(items)
    print()
    print(items["transaction_item"])
    print()
    if items["message_opt"] == "yes":
        print(items["message"])
        items.update({"message_opt": "no"})
    if items["menu_option"] == 'edit_menu':
        edit_select = tedit_menu(items)
        items.update({"menu_option": edit_select})
        system('clear')
        transaction_edit(items)
    if items["menu_option"] == '1':
        new_date = edit_one(items)        
        if new_date == 're-edit':
            system('clear')
            items.update({"menu_option": "edit_menu"})
            transaction_edit(items)
        else:
            system('clear')
            items.update({"data_load": "re-load"})
            items.update({"menu_option": "edit_menu"})
            items.update({"transaction_item": new_date})
            transaction_edit(items)
    elif items["menu_option"] == '2':
        new_transaction, new_balance = edit_two(items)        
        if new_transaction == 're-edit':
            system('clear')
            items.update({"menu_option": "edit_menu"})
            transaction_edit(items)
        else:
            system('clear')
            items.update({"transaction_item": new_transaction})
            items.update({"account_balance": new_balance})
            items.update({"data_load": "re-load"})
            items.update({"menu_option": "edit_menu"})
            transaction_edit(items)

    # change amount
    elif items["menu_option"] == '3':
        new_transaction, new_balance = edit_three(items)        
        if new_transaction == 're-edit':
            system('clear')
            items.update({"menu_option": "edit_menu"})
            transaction_edit(items)
        else:
            system('clear')
            items.update({"transaction_item": new_transaction})
            items.update({"account_balance": new_balance})
            items.update({"data_load": "re-load"})
            items.update({"menu_option": "edit_menu"})
            transaction_edit(items)

    # edit commnet
    elif items["menu_option"] == '4':
        transaction_update = edit_four(items)
        if transaction_update == 're-edit':
            system('clear')
            items.update({"menu_option": "edit_menu"})
            transaction_edit(items)
        else:
            system('clear')
            items.update({"transaction_item": transaction_update})
            items.update({"data_load": "re-load"})
            items.update({"menu_option": "edit_menu"})
            transaction_edit(items)

    # delete transaction
    elif items["menu_option"] == '5':
        transaction = items["transaction_item"]
        transaction_id = items["transaction_id"]
        new_balance = edit_five(items)
        if new_balance == 're-edit':
            system('clear')
            items.update({"menu_option": "edit_menu"})
            transaction_edit(items)
        else:
            system('clear')
            transaction_len = items["transaction_len"] - 1
            items.update({"data_load": "re-load"})
            items.update({"account_balance": new_balance})
            items.update({"transaction_len": transaction_len})
            transaction_menu(items)

    # return to menu
    elif items["menu_option"] == '6':
        system('clear')
        items.update({"menu_option": "edit_menu"})
        transaction_menu(items)

    # error message
    else:
        items.update({"message_opt": "yes"})
        items.update({"message": "Please enter a number between '1' and '6.'"})
        transaction_edit(items)



