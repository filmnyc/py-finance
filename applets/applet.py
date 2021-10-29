import re
from os import system
import json
import datetime
from accounts_info.models import engine, Account, db_session, Transaction

list_len = 5

# List of transactions of the selected account
# items = [action, account_name, account_balance, list_offset, transaction_len]
def transaction_list(selected_account, items):
    print('Transaction List')
    # print('e ' + str(len(items)))
    print()
    the_balance = '{:.2f}'.format(float(items[2]))
    print(f"\t{items[1]} {the_balance}")
    print()
    if items[0] == 're-load':
        if items[4] <= items[3]:
            trans_offset = 0
            e = 1
        elif items[4] > items[3] and items[4] < items[3] + list_len:
            trans_offset = items[4] - items[3]
            e = trans_offset + 1
        elif items[4] == items[3] + list_len:
            trans_offset = items[3]
            e= trans_offset + 1
        elif items[4] > items[3] + list_len:
            the_gap = items[4] - (items[3] +list_len)
            if the_gap >= list_len:
                trans_offset = (2 * list_len) + the_gap - list_len
                e = trans_offset + 1

        def alchemyencoder(obj):
            """JSON encoder function for SQLAlchemy special classes."""
            if isinstance(obj, datetime.date):
                return obj.isoformat()

        transaction_data = engine.execute('select * from transaction where account_id = {} order by cdate ASC limit {} offset {};'.format(selected_account, list_len, trans_offset))

        transaction_json = json.dumps([dict(r) for r in transaction_data], default=alchemyencoder)
        transaction_num = trans_offset + 1
    else:
        transaction_json = items[5]
        transaction_num = items[6]
        e = items[6]
    transactions = json.loads(transaction_json)

    for transact in transactions:
        transact_amount = '{:.2f}'.format(float(transact["amount"]))
        transact_cdate = datetime.datetime.strptime(transact["cdate"], "%Y-%m-%d").strftime('%m/%d/%Y')
        print(f'{e}) {transact_cdate} {transact["action"]} {transact_amount} - "{transact["comment"]}"')
        e = e + 1

    return transaction_json, transaction_num

# Check for "yes" or "no" action=comment(what you want to do), entity=on a variable, selectedname on object.
def while_yn(action, entity, account_name):
    process_it = ''
    while not process_it == 'y' and not process_it == 'n':
        if process_it == 'y' or process_it == 'n':
            pass 
        else:
            print()
            print('"' + action + ' ' + entity + '? \'y\' or \'n\'"')
    return process_it    

# Currancy check for Create Account, Withdraw/Deposit, Edit Transaction
def currency(show):
    message = ''
    while show == 'y':
        print(message)
        amount = input('Amount: ')
        if amount.replace('.', '', 1).isdigit() == False:
            message = '\n "The amount must be in digits"'
            show = 'y'
        elif '.' not in amount:
            new_amount = amount
            show = 'n'
            return new_amount
        else:
            d_cents = amount.split('.')
            if len(d_cents[1]) > 2:
                message = '\n"Amount should be formated as currency"'
                show = 'y'
            else:
                new_amount = amount
                show = 'n'
                return new_amount


# 'yes' and 'no' function
def go_ahead(statement):
    approve_it = ''
    while not approve_it == 'y' and not approve_it == 'n':
        approve_it = input(statement + ' (y/n) ')
        if approve_it == 'y' or approve_it == 'n':
            pass 
        else:
            print('"' + statement + '? \'y\' or \'n\'"')
    return approve_it    

def account_list(items):
    print('\tAccount list')
    print(items["data_load"])
    all_accounts_len = db_session.query(Account).count()
    if items["data_load"] == 're-load':
        if items["alter_list"] == list_len:
            trans_offset = 0
            e = 1
        else:
            if all_accounts_len < items["alter_list"]:
                trans_offset = all_accounts_len - list_len  
                e = trans_offset + 1
            elif all_accounts_len >= items["alter_list"]:
                trans_offset = items["alter_list"] - list_len
                e= trans_offset + 1

        account_data = engine.execute('select * from account order by id limit {} offset {};'.format(list_len, trans_offset))

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

    # items = {"data_load": "load", "account_len": items["account_len"], "accounts_json": all_accounts_json, "account_num": account_list_num, "alter_list": items["alter_list"]}
    items.update({"data_load": "load", "accounts_json": all_accounts_json, "account_num": account_list_num, "account_len": all_accounts_len})
    return items
# def trans_header(selected, selected_transaction, page):
#     selected_account = account_name(selected)
# 
#         #Open selected account
#     transact_item = list_transactions(selected_account)
#     tran = transact_item[int(selected_transaction)]
#     tran = tran.split(' ')
#     if selected_transaction == '1':
#         tran_3 = tran[4]
#     else:
#         tran_3 = tran[3]
#     tran_0 = tran[0]
#     if selected_transaction == '1':
#         tran_1 = 'account opened'
#     else:
#         tran_1 = tran[1]
#     trim = re.compile(r'[^\d.,]+')
#     mystring = tran_3
#     tran_3 = trim.sub('', mystring)
#     
#     transaction_list(selected, page)
#     print() 
#     print(selected_transaction + ') ' + tran_0 + ' ' + tran_1 + ' - $' + tran_3)
#     print()
#     return tran_0, tran_1, tran_3
# 
# 
# 
# # Select transaction for editing or deleting
# def select_transaction(selected, page):
#     selected_account = account_name(selected)
#     transact_len = list_transactions(selected_account)
#     a = len(transact_len) - (int(page) + 1)
#     b = a + 5
#     if a <= 1:
#         low = a
#     else:
#         low = 0
#     send_transaction = ''
#     message = ''
#     while send_transaction == '':
#         print(message)
#         print()
#         print('Select Transaction (' + str(a + 1 - low) + ' - ' + str(a + 5) + ')')
#         print('Return (r):')
#         print()
#         the_transaction = input('Select: ')
#         print(the_transaction)
#         if the_transaction == 'r':
#             send_transaction = 'go_back'
#             system('clear')
#             return send_transaction
#         elif the_transaction.isnumeric() == False:
#             system('clear')
#             transaction_list(selected, page)
#             print()
#             message = '"Submit a \'number\' or (r)"'
#         elif int(the_transaction) < a + 1 - low or int(the_transaction) > (a + 5):
#             system('clear')
#             transaction_list(selected, page)
#             print()
#             message = '"Submit number within range" '
#         else:
#             send_transaction = the_transaction
#             system('clear')
#             return send_transaction
