import time
import sys
from os import system, rename, remove
from .models import Account, db_session, engine
from applets.applet import while_yn, go_ahead, account_list


# save_path = 'bank_accounts/'
# information_file = 'information/'

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
        print('Change title from ' + items["account_name"] + ' to')
        print()
        new_name = input('New title: ')
        edit_it = go_ahead('Change ' + items["account_name"] + ' to ' + new_name)
        if edit_it == 'y':
            rename_account = Account.query.get(items["selected_account"])
            rename_account.name = new_name
            db_session.commit()
            return 'good'
        else:
            return 'reject' 
