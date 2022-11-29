from os import system
import sys
from .transaction_fuctions import (select_transaction,
                                   transaction_list, trans_act1, trans_act2,
                                   trans_act3, trans_act4, trans_act5)
from .account_fuctions import (create_account, change_account, account_select,
                               account_list)
from .transaction_edit import (tedit_menu, edit_one, edit_two, edit_three,
                               edit_four, edit_five, edit_two_show)
from rich import print
from applets.applet import selector
from .models import Account, db_session, engine, Transaction
from .transfer import (transfer_one, transfer_two, transfer_three,
                      transfer_four, transfer_five)
from rich.console import Console
from rich.table import Table


def account_menu(items):
    system('clear')
    items = account_list(items)
    print(items["account_len"])
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
        if items["message_opt"] == 'yes':
            account_menu(items)
        else:
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
        items = transfer_menu(items)
    print('Account menu')
    # print(items["alter_list"])
    print(items["account_len"])
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
    print(' Transfer (t)')
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
            items.update({"data_load": "re-load", "menu_option": "menu"})
            account_menu(items)
    elif choice == 'a':
        items.update({"menu_option": "delete"})
        account_menu(items)
    elif choice == 't':
        items.update({"menu_option": "transfer_one"})
        account_menu(items)
    elif choice == 'e':
        items.update({"menu_option": "edit"})
        account_menu(items)
    else:
        items.update({"message_opt": "yes", "message":
                      "\"Enter a correct letter\""})
        account_menu(items)


def transfer_menu(items):
    if items["menu_option"] == 'transfer_one':
        items = transfer_one(items)
        account_menu(items)
    elif items["menu_option"] == 'transfer_two':
        items = transfer_two(items)
        account_menu(items)
    elif items["menu_option"] == 'transfer_three':
        items = transfer_three(items)
        account_menu(items)
    elif items["menu_option"] == 'transfer_four':
        items = transfer_four(items)
        account_menu(items)
    elif items["menu_option"] == 'transfer_five':
        items = transfer_five(items)
        account_menu(items)
    

def transaction_menu(items):
    system('clear')
    print()
    items = transaction_list(items)
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
            items.update({"message_opt": "yes", "message": "\"Selection\
                         out of range\""})
            transaction_menu(items)
    elif change == "e":
        system('clear')
        items.update({"menu_option": "select"})
        transaction_menu(items)
    elif change == "a":
        items.update({"action": "Deposit", "menu_option": "trans_act1"})
        items = trans_act(items)
    elif change == "w":
        items.update({"action": "Withdraw", "menu_option": "trans_act1"})
        items = trans_act(items)
    elif change == "m":
        items.update({"data_load": "re-load", "menu_option": "menu",})
        account_menu(items)
    elif change == "q":
        print("\nExiting...")
        sys.exit()
    else:
        system('clear')
        items.update({"message_opt": "yes", "message": "\"Invalid input\""})
        print(items["message"])
        transaction_menu(items)

def trans_act(items):
    system('clear')
    print()
    items = transaction_list(items)
    print()
    if items["message_opt"] == "yes":
        print()
        print(items["message"])
        print()
        items.update({"message_opt": "no"})
    else:
        pass
    if items["menu_option"] == "trans_act1":
        items = trans_act1(items)
        trans_act(items)
    if items["menu_option"] == "trans_act2":
        items = trans_act2(items)
        trans_act(items)
    if items["menu_option"] == "trans_act3":
        items = trans_act3(items)
        trans_act(items)
    if items["menu_option"] == "trans_act4":
        items = trans_act4(items)
        trans_act(items)
    if items["menu_option"] == "trans_act5":
        items = trans_act5(items)
        transaction_menu(items)
    if items["menu_option"] == "menu":
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
        print()
        items.update({"message_opt": "no"})
    if items["menu_option"] == 'edit_menu':
        items = tedit_menu(items)
        transaction_edit(items)
    if items["menu_option"] == '1':
        items = edit_one(items)
        transaction_edit(items)
    elif items["menu_option"] == '2':
        items = edit_two(items)
        transaction_edit(items)
    elif items["menu_option"] == '2_show':
        items = edit_two_show(items)
        transaction_edit(items)

    # change amount
    elif items["menu_option"] == '3':
        items = edit_three(items)
        system('clear')
        transaction_edit(items)

    # edit commnet
    elif items["menu_option"] == '4':
        items = edit_four(items)
        transaction_edit(items)

    # delete transaction
    elif items["menu_option"] == '5':
        items = edit_five(items)
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
