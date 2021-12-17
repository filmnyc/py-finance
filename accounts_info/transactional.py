from os import system
# from account_data.accounts_db import account_name, list_transactions, transaction_add, account_balance, balance_update, transaction_list
import time
import datetime
from applets.applet import currency, while_yn, go_ahead, transaction_list
from .models import engine, Account, Transaction, db_session
from sqlalchemy import func

# items = [action, account_name, account_balance, list_offset, transaction_len, transaction_json, transaction_num]

        # items = [action, account_name, account_balance, alter_list, transaction_len, transaction_json, transaction_num]
#            items = {"data_load": "re-load", "account_name": account_name, \
#                    "account_balance": account_balance, "alter_list": alter_list, \
#                    "transaction_len": transaction_len, "selected_account": \
#                    selected_account, "menu_option": "transaction", "message_opt": \
#                    "no", "message": " ", "transaction_json": " ", "transaction_num, \
#                    "menu_opt": " "}
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
        print('The new transaction: ' + trans_time + ' ' + items["menu_option"] + ' - ' + amount_show + ' \"' + rec_comment + '\"')
    else:
        print()
        print('The new transaction: ' + trans_time + ' ' + items["menu_option"] + ' - ' + amount_show)
    old_balance = Transaction.query.with_entities(func.sum(Transaction.amount).filter(Transaction.account_id == items["selected_account"]).label('total')).first().total
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
    print(items["account_name"] + ' balance of ' + old_balance_show + ' will be updated to ' + new_balance_show)
    if items["menu_option"] == 'Withdraw':
        db_amount = '-' + str(amount)
    else:
        db_amount = amount
    record_it = go_ahead("Record this transaction?")
    if record_it == 'y':
        trans_time = time.strftime('%m/%d/%Y')
        db_date = datetime.datetime.strptime(trans_time, '%m/%d/%Y')
        new_transaction = Transaction(action=items["menu_option"], amount=db_amount, cdate=db_date, comment=rec_comment, account_id=items["selected_account"])
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


#def while_yn(dorw, selected_name):
#    transact_it = ''
#    while not transact_it == 'y' and not transact_it == 'n':
#        transact_it = input('Add a ' + dorw + ' to ' + selected_name + '? (y/n) ')
#        if transact_it == 'y' or transact_it == 'n':
#            pass 
#        else:
#            print('"Make a ' + dorw + '? \'y\' or \'n\'"')
#    return transact_it    

#transact(3, 'Withdraw', 5)
