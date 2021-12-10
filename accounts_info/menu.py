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
        elif items["message_opt"] == 'yes':
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
            items({"menu_option": "menu"})
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
        transaction_len = db_session.query(Transaction).filter_by(account_id = selected_account).count()
        if items["menu_option"] == 'select':
            alter_list = 5
            # items = [action, account_name, account_balance, alter_list, transaction_len]
            items = ['re-load', account_name, account_balance, alter_list, transaction_len]
        #    print(items)
        #    print(selected_account)
        #    hello = input('hello')

            transaction_menu(selected_account, items)
        elif items["menu_option"] == 'delete':
            items.update({"account_listing": row[1], "selected_account": row[2]})
            change_it = change_account(items)
            if change_it == 'reject':
                account_menu(items)
            else:
                items.update({"data_load": "re-load"})
                account_menu(items)
        else: 
            items["menu_option"] == 'edit'
            items.update({"account_listing": row[1], "selected_account": row[2], "account_name": accounts["name"]})
            change_it = change_account(items)
            if change_it == 'reject':
                account_menu(items)
            else:
                items.update({"data_load": "re-load"})
                account_menu(items)
#            hello = input('hello')

# Select single transaction from list of transactions
# items = [action, account_name, account_balance, alter_list, transaction_len, transaction_json, transaction_num]
def select_transaction(selected_account, items):
    if items[7] == 'select':
        transaction_list(selected_account, items)
        if items[0] == 'message':
            print()
            print(items[8])
            items.remove(items[8])
        if items[6] + 4 <= items[4]: 
            list_end = 0
        else:
            list_end = items[4] - (items[6] + 4)
        print()
        print('Select Transaction (' + str(items[6]) + ' - ' + str(items[6] + 4 + list_end) + ')')
        print('Return (r):')
        print()
        selected_transaction = input('Select: ')
        system('clear')
        if selected_transaction == 'r':
            transaction_menu(selected_account, items)
        elif selected_transaction.isnumeric() == False:
            items[0] = 'message'
            the_message = '"Selection must be a \'number\'"'
            items.insert(len(items), the_message)
            select_transaction(selected_account, items)
        elif int(selected_transaction) < items[6] or int(selected_transaction) > (items[6] + 4 + list_end):
            items[0] = 'message'
            the_message = '"Selection must be within \'number\' range"'
            items.insert(len(items), the_message)
            select_transaction(selected_account, items)
        else:
            items = ['load', items[1], items[2], items[3], items[4], items[5], items[6], selected_transaction]
            select_transaction(selected_account, items)
    else:
        e = items[6]
        transactions = json.loads(items[5])

        for transact in transactions:
            transact_amount = '{:.2f}'.format(float(transact["amount"]))
            transact_cdate = datetime.datetime.strptime(transact["cdate"], "%Y-%m-%d").strftime('%m/%d/%Y')
            row = [e, f'{e}) {transact_cdate} {transact["action"]} {transact_amount} - "{transact["comment"]}"', transact["id"]]
            if row[0] == int(items[7]):
                break
            else:
                e = e + 1

        items = ['load', items[1], items[2], items[3], items[4], items[5], items[6], row[1], 'menu', row[2]]
        transaction_edit(selected_account, items)

# The menu under listed transaction
# items = [action, account_name, account_balance, alter_list, transaction_len, transaction_json, edit_menu, transaction_num]
def transaction_menu(selected_account, items):
    system('clear')
#    print(items)
#    print(selected_account)
#    hello = input('hello')
    transaction_json, transaction_num = transaction_list(selected_account, items)
    if items[0] == 'message':
        print()
        print(items[7])
    print('\nTransaction Menu\n')
    if not items[3] >= items[4]:
        print(' Page Up (u)')
    if items[3] - 5 > 0:
        print(' Page Down (d)')
    print(' Deposit (a)\n Withdraw (w)\n Edit/Delete Transaction (e)\n Main Menu (m)\n Quit (q)')
    print()
    change = str(input("Select: "))
    change = change.lower()
    if change == "u":
        if not items[3] >= items[4]:
            system('clear')
            alter_list = items[3] + list_len
            items = ['re-load', items[1], items[2], alter_list, items[4]]
            transaction_menu(selected_account, items)
        else:
            system('clear')
            the_message = ('"Selection out of range"')
            items = ['message', items[1], items[2], items[3], items[4], transaction_json, transaction_num, the_message]
            transaction_menu(selected_account, items)
    elif change == "d":
        if items[3] - 5 > 0:
            system('clear')
            items[3] = items[3] - 5
            items = ['re-load', items[1], items[2], items[3], items[4]]
            transaction_menu(selected_account, items)
        else:
            system('clear')
            the_message = ('"Selection out of range"')
            items = ['message', items[1], items[2], items[3], items[4], transaction_json, transaction_num, the_message]
            transaction_menu(selected_account, items)
    elif change == "e": 
        system('clear')
        # items = [action, account_name, account_balance, alter_list, transaction_len, transaction_json, transaction_num]
        items = ['load', items[1], items[2], items[3], items[4], transaction_json, transaction_num, 'select']
        select_transaction(selected_account, items)
    elif change == "a": 
        system('clear')
        items = ['Deposit', items[1], items[2], items[3], items[4], transaction_json, transaction_num]
        new_balance, transaction_len = trans_act(selected_account, items)
        if new_balance == 're-edit':
            items[0] = 'menu'
            transaction_menu(selected_account, items)
        else:
            items = ['re-load', items[1], new_balance, items[3], transaction_len]
            transaction_menu(selected_account, items)
    elif change == "w": 
        system('clear')
        items = ['Withdraw', items[1], items[2], items[3], items[4], transaction_json, transaction_num]
        new_balance, transaction_len = trans_act(selected_account, items)
        if new_balance == 're-edit':
            items[0] = 'menu'
            transaction_menu(selected_account, items)
        else:
            items = ['re-load', items[1], new_balance, items[3], transaction_len]
            transaction_menu(selected_account, items)
    elif change == "m":
        system('clear')
        items = {"data_load": "re-load", "alter_list": 5, "message_opt": "no", "message": ' '}
        account_menu(items)
    elif change == "q":
        print("\nExiting...")
        sys.exit()
    else:
        system('clear')
        the_message = ('"Invalid input"')
        items = ['message', items[1], items[2], items[3], items[4], transaction_json, transaction_num, the_message]
        transaction_menu(selected_account, items)


# Edit transaction menu
def transaction_edit(selected_account, items):
    transaction_list(selected_account, items)
    print()
    print(items[7])
    print()
    if items[8] == 'menu':
        edit_select = tedit_menu(selected_account, items)
        items[8] = edit_select
        system('clear')
        transaction_edit(selected_account, items)

    if items[8] == '1':
        new_date = edit_one(selected_account, items)        
        if new_date == 're-edit':
            system('clear')
            items[8] = 'menu'
            transaction_edit(selected_account, items)
        else:
            system('clear')
            items[0] = 're-load'
            items[8] = 'menu'
            items[7] = new_date
            transaction_edit(selected_account, items)

    elif items[8] == '2':
        new_transaction, new_balance = edit_two(selected_account, items)        
        if new_transaction == 're-edit':
            system('clear')
            items[8] = 'menu'
            transaction_edit(selected_account, items)
        else:
            system('clear')
            items[7] = new_transaction
            items[2] = new_balance
            items[0] = 're-load'
            items[8] = 'menu'
            transaction_edit(selected_account, items)

    # change amount
    elif items[8] == '3':
        transaction_id = items[9]
        new_transaction, new_balance = edit_three(selected_account, items, transaction_id)        
        if new_transaction == 're-edit':
            system('clear')
            items[8] = 'menu'
            transaction_edit(selected_account, items)
        else:
            system('clear')
            items[7] = new_transaction
            items[2] = new_balance
            items[0] = 're-load'
            items[8] = 'menu'
            transaction_edit(selected_account, items)

    # edit commnet
    elif items[8] == '4':
        transaction = items[7]
        transaction_id = items[9]
        transaction_update = edit_four(transaction, transaction_id)
        if transaction_update == 're-edit':
            system('clear')
            items[8] = 'menu'
            transaction_edit(selected_account, items)
        else:
            system('clear')
            items[7] = transaction_update
            items[0] = 're-load'
            items[8] = 'menu'
            transaction_edit(selected_account, items)

# items = [action, account_name, account_balance, list_offset, transaction_len, transaction_json, transaction_num]
    # delete transaction
    elif items[8] == '5':
        transaction = items[7]
        transaction_id = items[9]
        new_balance = edit_five(selected_account, transaction, transaction_id)
        if new_balance == 're-edit':
            system('clear')
            items[8] = 'menu'
            transaction_edit(selected_account, items)
        else:
            system('clear')
            transaction_len = items[4] - 1
            items = ['re-load', items[1], new_balance, items[3], transaction_len]
            transaction_menu(selected_account, items)
    else:
        items[8] == '6'
        system('clear')
        items = ['re-load', items[1], items[2], items[3], items[4]]
        transaction_menu(selected_account, items)



#account_list()
