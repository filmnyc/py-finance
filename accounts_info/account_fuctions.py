from os import system
from .models import Account, db_session, engine, Transaction
from applets.applet import go_ahead, selector
import json
from rich import print


def account_list(items):
    print('\tAccount list')
    print(items["data_load"])
    all_accounts_len = db_session.query(Account).count()
    if items["data_load"] == 're-load':
        if items["alter_list"] == items["list_len"]:
            trans_offset = 0
            e = 1
        else:
            if all_accounts_len < items["alter_list"]:
                if (all_accounts_len - items["list_len"]) < 0:
                    trans_offset = 0
                    e = 1
                else:
                    trans_offset = all_accounts_len - items["list_len"]
                    e = trans_offset + 1
            elif all_accounts_len >= items["alter_list"]:
                trans_offset = items["alter_list"] - items["list_len"]
                e = trans_offset + 1

        account_data = engine.execute('select * from account order by id limit {}\
                offset {};'.format(items["list_len"], trans_offset))

        account_json = json.dumps([dict(r) for r in account_data])

        account_list_num = trans_offset + 1
        all_accounts_json = json.loads(account_json)
    else:
        account_list_num = items["account_num"]
        e = items["account_num"]
        all_accounts_json = items["accounts_json"]

    for account in all_accounts_json:
        account_amount = '{:.2f}'.format(float(account["balance"]))
        print(f'{e}) {account["name"]} {account_amount}')
        e = e + 1

    items.update({"data_load": "load", "accounts_json": all_accounts_json,
                  "account_num": account_list_num, "account_len":
                  all_accounts_len})
    return items


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

    new_acct = Account(name=account_name, balance=.00)
    db_session.add(new_acct)
    db_session.commit()
    system('clear')
    return 'good'


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
            items.update({"menu_option": "menu"})
            return items
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
        edit_it = go_ahead('Change ' + items["account_name"] + ' to '
                           + new_name)
        if edit_it == 'y':
            rename_account = Account.query.get(items["selected_account"])
            rename_account.name = new_name
            db_session.commit()
            items.update({"data_load": "re-load"})
            items.update({"menu_option": "menu"})
            return items
        else:
            items.update({"menu_option": "menu"})
            return items


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
    elif select_account.isnumeric() is False:
        items.update({"message_opt": "yes", "message":
                      "\"Submit a number or (r)\""})
        return items
    elif int(select_account) < str_left or int(select_account) > str_right:
        items.update({"message_opt": "yes", "message":
                      "\"Submit number within range\""})
        return items
    else:
        e = items["account_num"]
        all_accounts = items["accounts_json"]

        for accounts in all_accounts:
            account_amount = '{:.2f}'.format(float(accounts["balance"]))
            row = ([e, f'{e}) {accounts["name"]} {account_amount}',
                   accounts["id"]])
            if row[0] == int(select_account):
                break
            else:
                e = e + 1
        selected_account = row[2]
        account_name = accounts["name"]
        account_balance = accounts["balance"]
        transaction_len = (db_session.query(Transaction).filter_by
                           (account_id=selected_account).count())
        list_len = items["list_len"]
        items.update({"account_name": account_name,
                      "account_balance": account_balance, "alter_list":
                      list_len,  "transaction_len": transaction_len,
                      "selected_account": selected_account, "message_opt":
                      "no", "message": " "})

        if items["menu_option"] == 'select':
            items.update({"menu_option": "transaction",
                          "data_load": "re-load"})
            return items
        elif items["menu_option"] == 'delete':
            items.update({"account_listing": row[1]})
            return items
        else:
            items["menu_option"] == 'edit'
            items.update({"account_listing": row[1]})
            return items
