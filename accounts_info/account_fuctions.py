import time
import sys
from os import system, rename, remove
from .models import Account, db_session, engine, Transaction
from applets.applet import while_yn, go_ahead, account_list, selector


def create_account(items):
    system('clear')
    account_list(items)
    print()
    print('Create account name: ')
    print('Return (r):')
    print()
    account_name = input('Name: ')
    if account_name == 'r':
        return 'reject'
    okay_it = go_ahead('If new account name "' + account_name + '" is okay?')
    if okay_it == 'y':
        pass
    else:
        return 'reject'

    new_acct = Account(name = account_name, balance=.00)
    db_session.add(new_acct)
    db_session.commit()
    system('clear')
    return 'good'

# Linked from menu mondule - list_menu
# items = [account_name, account_balance, account_number. action]
def change_account(items):
    account_list(items)
    print()
    print(items["account_listing"])
    print()
    if items["menu_option"] == 'delete':
        delete_it = go_ahead('Delete this account?')
        if delete_it == 'y':
            pass
        else:
            return 'reject'
        del_account = Account.query.get(items["selected_account"])
        db_session.delete(del_account)
        db_session.commit()
        items.update({"data_load": "re-load"})
        items.update({"menu_option": "menu"})
        return items

    if items["menu_option"] == 'edit':
        print('Change title from ' + items["account_name"] + ' to:')
        print()
        new_name = input('New title: ')
        edit_it = go_ahead('Change ' + items["account_name"] + ' to ' + new_name)
        if edit_it == 'y':
            rename_account = Account.query.get(items["selected_account"])
            rename_account.name = new_name
            db_session.commit()
            items.update({"data_load": "re-load"})
            items.update({"menu_option": "menu"})
            return items
        else:
            return 'reject' 

# select account menu - a number from 1 - 5
def account_select(items):
    if items["account_num"] > 0:
        select_string, str_left, str_right = selector(items)
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
  
        selected_account = row[2]
        account_name = accounts["name"]
        account_balance = accounts["balance"]
        account_number = select_account
        transaction_len = db_session.query(Transaction).filter_by(account_id = \
                selected_account).count()

        list_len = items["list_len"]
        items.update({"data_load": "re-load", "account_name": account_name, \
                "account_balance": account_balance, "alter_list": list_len, \
                "transaction_len": transaction_len, "selected_account": \
                selected_account, "message_opt": "no", "message": " "})

        if items["menu_option"] == 'select':
            items.update({"menu_option": "transaction"})
            return items
        elif items["menu_option"] == 'delete':
            items.update({"account_listing": row[1]})
            return items
        else: 
            items["menu_option"] == 'edit'
            items.update({"account_listing": row[1]})
            return items
