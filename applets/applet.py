import json
import datetime
from accounts_info.models import engine


def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()


# list of transactions of the selected account
def transaction_list(items):
    print('Transaction List')
    print()
    the_balance = '{:.2f}'.format(float(items["account_balance"]))
    print(f"\t{items['account_name']} {the_balance}")
    print()
    if items["data_load"] == 're-load':
        if items["transaction_len"] <= items["list_len"]:
            trans_offset = 0
            e = 1
        else:
            if items["transaction_len"] - items["alter_list"] < 0:
                trans_offset = 0
                e = 1
                print("t-0")
            elif items["transaction_len"] > items["alter_list"] and \
                    items["transaction_len"] <= items["alter_list"] + \
                    items["list_len"]:
                trans_offset = items["transaction_len"] - items["alter_list"]
                e = trans_offset + 1
                print("t-1")
            elif items["transaction_len"] > items["alter_list"] + \
                    items["list_len"]:
                # if items["transaction_len"] - items["alter_list"] >= 0:
                trans_offset = items["transaction_len"] - items["alter_list"]
                e = trans_offset + 1
                print("t-2")

        transaction_data = engine.execute('select * from transaction where '
                                          'account_id = {} order by cdate '
                                          'ASC limit {} offset {};'.format
                                          (items["selected_account"],
                                           items["list_len"], trans_offset))

        transaction_json = json.dumps([dict(r) for r in transaction_data],
                                      default=alchemyencoder)
        transaction_num = trans_offset + 1
    else:
        transaction_json = items["transaction_json"]
        transaction_num = items["transaction_num"]
        e = items["transaction_num"]
    transactions = json.loads(transaction_json)

    for transact in transactions:
        transact_amount = '{:.2f}'.format(float(transact["amount"]))
        transact_cdate = (datetime.datetime.strptime
                          (transact["cdate"], "%Y-%m-%d").strftime('%m/%d/%Y'))
        print(f'{e}) {transact_cdate} {transact["action"]} {transact_amount} - \
"{transact["comment"]}"')
        e = e + 1

    return transaction_json, transaction_num


def selector(items):
    if items["account_len"] <= items["list_len"]:
        str_left = items["account_num"]
        str_right = items["account_len"]
        select_string = ('(' + str(str_left) + ' - ' + str(str_right) + ')')
    else:
        if items["account_len"] > items["list_len"] and \
                items["account_len"] < (items["list_len"] * 2):
            str_left = items["account_num"]
            str_right = items["account_num"] + 4
            select_string = ('(' + str(str_left) + ' - ' 
                             + str(str_right) + ')')
        else:
            str_left = items["account_num"]
            str_right = items["account_num"] + (items["list_len"] - 1)
            select_string = ('(' + str(str_left) + ' - ' +
                             str(str_right) + ')')
    return select_string, str_left, str_right


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
        if amount.replace('.', '', 1).isdigit() is False:
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
