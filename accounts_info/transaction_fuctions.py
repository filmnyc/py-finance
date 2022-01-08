from os import system
import time
import datetime
from applets.applet import currency, while_yn, go_ahead, transaction_list
from .models import engine, Account, Transaction, db_session
from sqlalchemy import func
import json

def trans_act(items):
    print()
    transaction_list(items)
    print()
    print('\tMake a ' + items["menu_option"])
    print()
    print('Enter amount for the ' + items["menu_option"])
    amount = currency('y')
    amount_show = '{:.2f}'.format(float(amount))
    trans_time = time.strftime('%m/%d/%Y')
    new_transaction = trans_time + ' ' + items["menu_option"] + ' - ' + amount_show
    print(new_transaction)
    okay_it = go_ahead("If this is okay enter?")
    if okay_it == 'y':
        pass
    else:
        system('clear')
        return 're-edit', 're-edit'
    print()
    add_comment = go_ahead('Add a comment to this transaction??')
    if add_comment == 'y':
        print()
        rec_comment = input('Add comment: ')
        print()
        print('The new transaction: ' + trans_time + ' ' + items["menu_option"] \
+ ' - ' + amount_show + ' \"' + rec_comment + '\"')
    else:
        rec_comment = 'no comment'
        print()
        print('The new transaction: ' + trans_time + ' ' + items["menu_option"] \
+ ' - ' + amount_show)
    old_balance = Transaction.query.with_entities(func.sum(Transaction.amount).\
            filter(Transaction.account_id == items["selected_account"]).\
            label('total')).first().total
    amount = float(amount)
    if old_balance != None:
        old_balance = float(old_balance)
    else:
        old_balance = 0.00
    if items["menu_option"] == 'Deposit':
        new_balance = old_balance + amount
    else:
        new_balance = old_balance - amount
    new_balance_show = '{:.2f}'.format(float(new_balance))
    old_balance_show = '{:.2f}'.format(float(old_balance))
    print()
    print(items["account_name"] + ' balance of ' + old_balance_show + ' will be \
updated to ' + new_balance_show)
    if items["menu_option"] == 'Withdraw':
        db_amount = '-' + str(amount)
    else:
        db_amount = amount
    record_it = go_ahead("Record this transaction?")
    if record_it == 'y':
        trans_time = time.strftime('%m/%d/%Y')
        db_date = datetime.datetime.strptime(trans_time, '%m/%d/%Y')
        new_transaction = Transaction(action=items["menu_option"], amount=db_amount, \
                cdate=db_date, comment=rec_comment, account_id=items["selected_account"])
        db_session.add(new_transaction)
        db_session.commit()
        account_row = Account.query.get(items["selected_account"])
        account_row.balance = new_balance
        db_session.commit()
        system('clear')
        return new_balance, items["transaction_len"] + 1
    else:
        system('clear')
        return 're-edit', 're-edit'


def select_transaction(items):
    if items["menu_option"] == 'select':
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
            items.update({"menu_option": "menu"})
            return items
        elif selected_transaction.isnumeric() == False:
            items.update({"message_opt": "yes", "message": '"Selection must be a \'number\'"'})
            return items
        elif int(selected_transaction) < items["transaction_num"] or \
                int(selected_transaction) > (items["transaction_num"] + 4 + list_end):
            items.update({"message_opt": "yes", "message": '"Selection must \
                    be within \'number\' range"'})
            return items
        else:
            items.update({"menu_option": "selected", "selected_transaction": \
                    selected_transaction})
            return items
    else:
        e = items["transaction_num"]
        transactions = json.loads(items["transaction_json"])

        for transact in transactions:
            transact_amount = '{:.2f}'.format(float(transact["amount"]))
            transact_cdate = datetime.datetime.strptime(transact["cdate"], \
                    "%Y-%m-%d").strftime('%m/%d/%Y')
            row = ([e, f'{e}) {transact_cdate} {transact["action"]} {transact_amount} - \
"{transact["comment"]}"', transact["id"]])
            if row[0] == int(items["selected_transaction"]):
                break
            else:
                e = e + 1

        items.update({"menu_option": "edit_menu", "transaction_id": row[2], \
                "transaction_item": row[1]})
        return items
