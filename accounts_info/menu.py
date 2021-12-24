import datetime
from os import system
import sys
from .transactional import trans_act
from .account_fuctions import create_account, change_account
from .transaction_edit import tedit_menu, edit_one, edit_two, edit_three, edit_four, edit_five
from applets.applet import transaction_list, account_list, selector
from .models import engine, Account, db_session, Transaction
from sqlalchemy import func
import json
import decimal, datetime

list_len = 5


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
    if items["account_len"] <= list_len:
        pass
    else:
        if items["alter_list"] < items["account_len"]:
            print(' Move down (d) ')
        else:
            pass
        if items["alter_list"] >= items["account_len"]:
            print(' Move up (u)')
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
            new_list = items["alter_list"] + 5
            items.update({"alter_list": new_list, "data_load": "re-load"})
            account_menu(items)
    elif choice == 'u':
        if items["alter_list"] < items["account_len"]:
            items.update({"message_opt": "yes", "message": "Wrong direction"})
            account_menu(items)
        else:
            new_list = items["alter_list"] - 5
            items.update({"alter_list": new_list, "data_load": "re-load"})
            account_menu(items)
    elif choice == 's':
        items.update({"menu_option": "select"})
        account_menu(items)
       # the_account = account_menu(items)
       # if the_account == 're-select':
       #     items({"menu_option": "menu"})
       #     account_menu(items)
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



# select account menu - a number from 1 - 5
def account_select(items):
#    system('clear')
#    account_list(items)
#    print()
#    if items["message_opt"] == 'yes':
#        print(items["message"])
#        print()

    if items["account_num"] > 0:
        select_string, str_left, str_right = selector(items, list_len)
        print(select_string)
    print('Return (r):')
    print()
    select_account = input('Select account: ')
    system('clear')
    if select_account == 'r':
        items.update({"menu_option": "menu"})
        return items
    elif select_account.isnumeric() == False:
        items.update({"message_opt": "yes", "message": "\"Submit a number or (r)\""})
        return items
    elif int(select_account) < str_left or int(select_account) > str_right:
        items.update({"message_opt": "yes", "message": "\"Submit number within \
range\""})
        return items
    else:
        e = items["account_num"]
        all_accounts = items["accounts_json"]

        for accounts in all_accounts:
            account_amount = '{:.2f}'.format(float(accounts["balance"]))
            row = [e, f'{e}) {accounts["name"]} {account_amount}', accounts["id"]]
            if row[0] == int(select_account):
                break
            else:
                e = e + 1
  
#        print(accounts["name"])
        selected_account = row[2]
        account_name = accounts["name"]
        account_balance = accounts["balance"]
        account_number = select_account
        transaction_len = db_session.query(Transaction).filter_by(account_id = \
                selected_account).count()
        if items["menu_option"] == 'select':
            alter_list = 5
            # items = [action, account_name, account_balance, alter_list, transaction_len]
#            items = ['re-load', account_name, account_balance, alter_list, \
#                    transaction_len]
            items = {"data_load": "re-load", "account_name": account_name, \
                    "account_balance": account_balance, "alter_list": alter_list, \
                    "transaction_len": transaction_len, "selected_account": \
                    selected_account, "menu_option": "transaction", "message_opt": \
                    "no", "message": " "}
            return items
        elif items["menu_option"] == 'delete':
            items.update({"account_listing": row[1], "selected_account": \
                    selected_account})
            return items
        else: 
            items["menu_option"] == 'edit'
            items.update({"account_listing": row[1], "selected_account": row[2]})
            return items

# Select single transaction from list of transactions
# items = [action, account_name, account_balance, alter_list, transaction_len, transaction_json, transaction_num]
        # items = [action, account_name, account_balance, alter_list, transaction_len, transaction_json, transaction_num]
#            items = {"data_load": "re-load", "account_name": account_name, \
#                    "account_balance": account_balance, "alter_list": alter_list, \
#                    "transaction_len": transaction_len, "selected_account": \
#                    selected_account, "menu_option": "transaction", "message_opt": \
#                    "no", "message": " ", "transaction_json": " ", "transaction_num, \
#                    "menu_opt": " "}
def select_transaction(items):
    if items["menu_option"] == 'select':
        transaction_list(items)
        if items["message_opt"] == 'yes':
            print()
            print(items["message"])
            items.update({"message_opt": "no"})
        if items["transaction_num"] + 4 <= items["transaction_len"]: 
            list_end = 0
        else:
            list_end = items["transaction_len"] - (items["transaction_num"] + 4)
        print()
        print('Select Transaction (' + str(items["transaction_num"]) + ' - ' + \
                str(items["transaction_num"] + 4 + list_end) + ')')
        print('Return (r):')
        print()
        selected_transaction = input('Select: ')
        system('clear')
        if selected_transaction == 'r':
            transaction_menu(items)
        elif selected_transaction.isnumeric() == False:
            items.update["message_opt": "yes", "message": '"Selection must be a \'number\'"']
            select_transaction(items)
        elif int(selected_transaction) < items["transaction_num"] or \
                int(selected_transaction) > (items["transaction_num"] + 4 + list_end):
            items.update({"message_opt": "yes", "message": '"Selection must be within \'number\' range"'})
            select_transaction(items)
        # items = [action, account_name, account_balance, alter_list, transaction_len, transaction_json, transaction_num]
#            items = {"data_load": "re-load", "account_name": account_name, \
#                    "account_balance": account_balance, "alter_list": alter_list, \
#                    "transaction_len": transaction_len, "selected_account": \
#                    selected_account, "menu_option": "transaction", "message_opt": \
#                    "no", "message": " ", "transaction_json": " ", "transaction_num, \
#                    "menu_opt": " "}
        else:
            items.update({"menu_option": "selected", "selected_transaction": selected_transaction})
            return items
    else:
        e = items["transaction_num"]
        transactions = json.loads(items["transaction_json"])

        for transact in transactions:
            transact_amount = '{:.2f}'.format(float(transact["amount"]))
            transact_cdate = datetime.datetime.strptime(transact["cdate"], "%Y-%m-%d").strftime('%m/%d/%Y')
            row = ([e, f'{e}) {transact_cdate} {transact["action"]} {transact_amount} - \
"{transact["comment"]}"', transact["id"]])
            if row[0] == int(items["selected_transaction"]):
                break
            else:
                e = e + 1
        # items = [action, account_name, account_balance, alter_list, transaction_len, transaction_json, transaction_num]
#            items = {"data_load": "re-load", "account_name": account_name, \
#                    "account_balance": account_balance, "alter_list": alter_list, \
#                    "transaction_len": transaction_len, "selected_account": \
#                    selected_account, "menu_option": "transaction", "message_opt": \
#                    "no", "message": " ", "transaction_json": " ", "transaction_num, \
#                    "menu_opt": " "}

        items.update({"menu_option": "menu", "transaction_id": row[2], "transaction_item": \
                row[1]})
        # print(items["transaction_item"])
        # hello = input('hello')
        return items

# The menu under listed transaction
# items = [action, account_name, account_balance, alter_list, transaction_len, transaction_json, edit_menu, transaction_num]
def transaction_menu(items):
    system('clear')
#    print(items)
#    print(selected_account)
#    hello = input('hello')
    transaction_json, transaction_num = transaction_list(items)
    if items["message_opt"] == 'yes':
        print()
        print(items["message"])
        items.update({"message_opt": "no"})
    print('\nTransaction Menu\n')
    if not items["alter_list"] >= items["transaction_len"]:
        print(' Page Up (u)')
    if items["alter_list"] - 5 > 0:
        print(' Page Down (d)')
    print(' Deposit (a)\n Withdraw (w)\n Edit/Delete Transaction (e)\n Main Menu (m)\n Quit (q)')
    print()
    change = str(input("Select: "))
    change = change.lower()
    if change == "u":
# items = [action, account_name, account_balance, alter_list, transaction_len, transaction_json, edit_menu, transaction_num]

#            items = {"data_load": "re-load", "account_name": account_name, \
#                    "account_balance": account_balance, "alter_list": alter_list, \
#                    "transaction_len": transaction_len, "selected_account": \
#                    selected_account, "menu_option": "transaction", "message_opt": \
#                    "no", "message": " "}
        if not items["alter_list"] >= items["transaction_len"]:
            system('clear')
            alter_list = items["alter_list"] + list_len
            items.update({"data_load": "re-load", "alter_list": alter_list})
            transaction_menu(items)
        else:
            system('clear')
            items.update({"message_opt": "yes", "message": "\"Selection out of range\""})
            transaction_menu(items)
    elif change == "d":
        if items["alter_list"] - 5 > 0:
            system('clear')
            alter_list = items["alter_list"] - 5
            items.update({"data_load": "re-load", "alter_list": alter_list})
            transaction_menu(items)
        else:
            system('clear')
            items.update({"message_opt": "yes", "message": "\"Selection out of range\""})
            transaction_menu(items)
    elif change == "e": 
        system('clear')
        # items = [action, account_name, account_balance, alter_list, transaction_len, transaction_json, transaction_num]
#            items = {"data_load": "re-load", "account_name": account_name, \
#                    "account_balance": account_balance, "alter_list": alter_list, \
#                    "transaction_len": transaction_len, "selected_account": \
#                    selected_account, "menu_option": "transaction", "message_opt": \
#                    "no", "message": " ", "transaction_json": " ", "transaction_num, \
#                    }
        items.update({"transaction_json": transaction_json, "transaction_num": \
                transaction_num, "menu_option": "select"})
        items = select_transaction(items)
        items = select_transaction(items)
        transaction_edit(items)
    elif change == "a": 
        system('clear')
        # items = ['Deposit', items[1], items[2], items[3], items[4], transaction_json, transaction_num]
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
        items = {"data_load": "re-load", "alter_list": 5, "message_opt": "no", \
                "message": ' ', "menu_option": "menu"}
        account_menu(items)
    elif change == "q":
        print("\nExiting...")
        sys.exit()
    else:
        system('clear')
        # message = ('"Invalid input"')
        items.update({"message_opt": "yes", "message": "\"Invalid input\""})
        print(items["message"])
        transaction_menu(items)

        # items = [action, account_name, account_balance, alter_list, transaction_len, transaction_json, transaction_num]
# items = {"data_load": "re-load", "account_name": account_name, \
#         "account_balance": account_balance, "alter_list": alter_list, \
#         "transaction_len": transaction_len, "selected_account": \
#         selected_account, "menu_option": "transaction", "message_opt": \
#         "no", "message": " ", "transaction_json": " ", "transaction_num, \
#          "menu_option": "menu", "transaction_id": row[2], "transaction_item":}

# Edit transaction menu
def transaction_edit(items):
    transaction_list(items)
    print()
    print(items["transaction_item"])
    print()
    if items["message_opt"] == "yes":
        print(items["message"])
        items.update({"message_opt": "no"})
    if items["menu_option"] == 'menu':
        edit_select = tedit_menu(items)
        items.update({"menu_option": edit_select})
        system('clear')
        transaction_edit(items)

    if items["menu_option"] == '1':
        new_date = edit_one(items)        
        if new_date == 're-edit':
            system('clear')
            items.update({"menu_option": "menu"})
            transaction_edit(items)
        else:
            system('clear')
            items.update({"data_load": "re-load"})
            items.update({"menu_option": "menu"})
            items.update({"transaction_item": new_date})
            transaction_edit(items)

    elif items["menu_option"] == '2':
        new_transaction, new_balance = edit_two(items)        
        if new_transaction == 're-edit':
            system('clear')
            items.update({"menu_option": "menu"})
            transaction_edit(items)
        else:
            system('clear')
            items.update({"transaction_item": new_transaction})
            items.update({"account_balance": new_balance})
            items.update({"data_load": "re-load"})
            items.update({"menu_option": "menu"})
            transaction_edit(items)

    # change amount
    elif items["menu_option"] == '3':
        # transaction_id = items["transaction_id"]
        new_transaction, new_balance = edit_three(items)        
        if new_transaction == 're-edit':
            system('clear')
            items.update({"menu_option": "menu"})
            transaction_edit(items)
        else:
            system('clear')
            items.update({"transaction_item": new_transaction})
            items.update({"account_balance": new_balance})
            items.update({"data_load": "re-load"})
            items.update({"menu_option": "menu"})
            transaction_edit(items)

    # edit commnet
    elif items["menu_option"] == '4':
        # transaction = items[7]
        # transaction_id = items[9]
        transaction_update = edit_four(items)
        if transaction_update == 're-edit':
            system('clear')
            items.update({"menu_option": "menu"})
            transaction_edit(items)
        else:
            system('clear')
            items.update({"transaction_item": transaction_update})
            items.update({"data_load": "re-load"})
            items.update({"menu_option": "menu"})
            transaction_edit(items)

# items = [action, account_name, account_balance, list_offset, transaction_len, transaction_json, transaction_num]
    # delete transaction
    elif items["menu_option"] == '5':
        transaction = items["transaction_item"]
        transaction_id = items["transaction_id"]
        new_balance = edit_five(items)
        if new_balance == 're-edit':
            system('clear')
            items.update({"menu_option": "menu"})
            transaction_edit(items)
        else:
            system('clear')
            transaction_len = items["transaction_len"] - 1
            items.update({"data_load": "re-load"})
            items.update({"account_balance": new_balance})
            items.update({"transaction_len": transaction_len})
            transaction_menu(items)
    elif items["menu_option"] == '6':
        system('clear')
        items.update({"menu_option": "menu"})
        transaction_menu(items)
    else:
        items.update({"message_opt": "yes"})
        items.update({"message": "Please enter a number between '1' and '6.'"})
        transaction_edit(items)



#account_list()
