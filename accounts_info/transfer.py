from applets.applet import selector
from os import system
from .models import Account, db_session, engine, Transaction
from rich import print
import time
import datetime
from sqlalchemy import func


def transfer_one(items):
    print('Transfer From')
    print()
    if items["account_num"] > 0:
        select_string, str_left, str_right = selector(items)
        if items["account_len"] <= items["alter_list"]:
            pass
        else:
            print(' Move down (d) ')
        if items["alter_list"] > items["list_len"]:
            print(' Move up (u) ')
        else:
            pass
        print(' Select account ' + select_string)
    else:
        items.update({message_option: "yes", message: "Nothing to transfer \
                      from this account", "menu_option": "menu"})
        return items

    # elif items["account_num"] == 'transfer_from':
    print(' Return (r):')
    print()
    selection = input('Make Selection: ')
    system('clear')
    if selection == 'r':
        items.update({"menu_option": "menu"})
        return items
    elif selection == 'd':
        if items["alter_list"] >= items["account_len"]:
            items.update({"message_opt": "yes", "message": "Wrong direction",
                          "menu_option": "menu"})
            return items
        else:
            new_list = items["alter_list"] + items["list_len"]
            items.update({"alter_list": new_list, "data_load": "re-load"})
            return items
    elif selection == 'u':
        if items["alter_list"] == items["list_len"]:
            items.update({"message_opt": "yes", "message": "Wrong direction",
                          "menu_option": "menu"})
            return items
        else:
            new_list = items["alter_list"] - items["list_len"]
            items.update({"alter_list": new_list, "data_load": "re-load"})
            return items
    elif selection.isnumeric() is False:
        items.update({"message_opt": "yes", "message":
                      "\"Submit a number or (r)\""})
        return items
    elif int(selection) < str_left or int(selection) > str_right:
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
            if row[0] == int(selection):
                break
            else:
                e = e + 1
        selected_account = row[2]
        account_name = accounts["name"]
        account_balance = accounts["balance"]
        transaction_len = (db_session.query(Transaction).filter_by
                           (account_id=selected_account).count())
        list_len = items["list_len"]
        items.update({"from_name": account_name,
                      "from_balance": account_balance, "alter_list":
                      list_len,  "transaction_len": transaction_len,
                      "from_account": selected_account, "message_opt":
                      "no", "message": " ", "menu_option": "transfer_two",
                      "from_listing": row[1]})
        return items


def transfer_two(items):
    print('Transfer from ' + items["from_name"] + ' (' + 
          '{:.2f}'.format(float(items["from_balance"])) + ')')
    print('Return (r)')
    print()
    transfer_amt = input('Transfer Amount: ')
    if transfer_amt == 'r':
        items.update({"menu_option": "menu"})
        return items
    elif transfer_amt.replace('.', '', 1).isdigit() is False:
        items.update({"message_opt": "yes", "message":
                      "\"Submit a number or (r)\""})
        return items
    elif '.' in transfer_amt:
        d_cents = transfer_amt.split('.')
        if len(d_cents[1]) > 2:
            items.update({"message_opt": "yes", "message":
                          "\"Amount should be formated as currency\""})
            return items
        else:
            items.update({"transfer_amt": transfer_amt, "menu_option":
                          "transfer_three"})
            return items

    else:
        items.update({"transfer_amt": transfer_amt, "menu_option":
                      "transfer_three"})
        return items


def transfer_three(items):
    print('Transfer from ' + items["from_name"] + ' (' + '{:.2f}'
          .format(float(items["from_balance"])) + ')' + ' for the amount of '
          + ('{:.2f}'.format(float(items["transfer_amt"]))))
    print()
    select_string, str_left, str_right = selector(items)
    print('Transfer To')
    print()
    if items["account_len"] <= items["alter_list"]:
        pass
    else:
        print(' Move down (d) ')
    if items["alter_list"] > items["list_len"]:
        print(' Move up (u) ')
    else:
        pass
    print(' Select account ' + select_string)
    print(' Return (r)')
    print()
    selection = input('Make Selection: ')
    system('clear')
    if selection == 'r':
        items.update({"menu_option": "menu"})
        return items
    elif selection == 'd':
        if items["alter_list"] >= items["account_len"]:
            items.update({"message_opt": "yes", "message": "Wrong direction",
                          "menu_option": "menu"})
            return items
        else:
            new_list = items["alter_list"] + items["list_len"]
            items.update({"alter_list": new_list, "data_load": "re-load"})
            return items
    elif selection == 'u':
        if items["alter_list"] == items["list_len"]:
            items.update({"message_opt": "yes", "message": "Wrong direction",
                          "menu_option": "menu"})
            return items
        else:
            new_list = items["alter_list"] - items["list_len"]
            items.update({"alter_list": new_list, "data_load": "re-load"})
            return items
    elif selection.isnumeric() is False:
        items.update({"message_opt": "yes", "message":
                      "\"Submit a number or (r)\""})
        return items
    elif int(selection) < str_left or int(selection) > str_right:
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
            if row[0] == int(selection):
                break
            else:
                e = e + 1
        selected_account = row[2]
        account_name = accounts["name"]
        account_balance = accounts["balance"]
        transaction_len = (db_session.query(Transaction).filter_by
                           (account_id=selected_account).count())
        list_len = items["list_len"]
        items.update({"to_name": account_name,
                      "to_balance": account_balance, "alter_list":
                      list_len,  "transaction_len": transaction_len,
                      "to_account": selected_account, "message_opt":
                      "no", "message": " ", "menu_option": "transfer_four",
                      "to_listing": row[1]})
        return items


def transfer_four(items):
    print('Transfer ' + ('{:.2f}'.format(float(items["transfer_amt"]))) +
          ' from ' + items["from_name"] + ' (' + '{:.2f}'.format(float(items
          ["from_balance"])) + ') to ' + items["to_name"] + ' (' + '{:.2f}'
          .format(float(items["to_balance"])) + ')')
    print()
    print('Transfer')
    print()
    print(' Make this transfer (y/n)')
    print()
    selection = input('Selection: ')
    if selection == 'y' or selection == 'n':
        pass
    else:
        items.update({"message_opt": 'yes', "message": ("\"Enter either \'y\'"
                                                        " or \'n\'\"")})
        return items
    if selection == 'n':
        items.update({"menu_option": "menu"})
        return items
    else:
        trans_time = time.strftime('%m/%d/%Y')
        db_date = datetime.datetime.strptime(trans_time, '%m/%d/%Y')
        from_comment = 'transfered to ' + items["to_name"]
        from_transaction = (Transaction(action='Transfer',
                            amount='-' + items["transfer_amt"], cdate=db_date,
                            comment=from_comment, account_id=items
                            ["from_account"]))
        db_session.add(from_transaction)
        to_comment = 'transfered from ' + items["from_name"]
        to_transaction = (Transaction(action='Transfer',
                          amount=items["transfer_amt"], cdate=db_date,
                          comment=to_comment, account_id=items
                          ["to_account"]))
        db_session.add(to_transaction)
        db_session.commit()
        from_balance = (Transaction.query.with_entities(func.sum
                       (Transaction.amount).filter
                       (Transaction.account_id == items
                        ["from_account"]).label('total')).first().
                       total)
        to_balance = (Transaction.query.with_entities(func.sum
                       (Transaction.amount).filter
                       (Transaction.account_id == items
                        ["to_account"]).label('total')).first().
                       total)
        from_row = Account.query.get(items["from_account"])
        from_row.balance = from_balance
        to_row = Account.query.get(items["to_account"])
        to_row.balance = to_balance
        db_session.commit()
        items.update({"to_balance": to_balance, "from_balance":
                      from_balance, "menu_option": "transfer_five",
                      "data_load": "re-load"})
        return items


def transfer_five(items):
    print(' New balance of ' + items["from_name"] + ' is ' +
          '{:.2f}'.format(float(items["from_balance"])))
    print()
    print(' New balance of ' + items["to_name"] + ' is ' +
          '{:.2f}'.format(float(items["to_balance"])))
    print()
    input('Okay?')
    items.update({"menu_option": "menu"})
    return items

        # hello = input('hello')


