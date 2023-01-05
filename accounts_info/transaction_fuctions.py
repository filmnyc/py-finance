from os import system
import time
import datetime
from applets.applet import currency, go_ahead
from .transaction_edit import date_maker
from .models import engine, Account, Transaction, db_session
from sqlalchemy import func
import json
from rich import print
from rich.console import Console
from rich.table import Table

table = Table()

def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()


def transaction_list(items):
    print(items["data_load"])
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
            elif (items["transaction_len"] > items["alter_list"] and
                  items["transaction_len"] <= items["alter_list"] +
                  items["list_len"]):
                trans_offset = items["transaction_len"] - items["alter_list"]
                e = trans_offset + 1
            else:
                trans_offset = items["transaction_len"] - items["alter_list"]
                e = trans_offset + 1

        transaction_data = (engine.execute('select * from transaction where \
                            account_id = {} order by cdate ASC limit {} \
                            offset {};'.format(items["selected_account"],
                            items["list_len"], trans_offset)))

        transaction_json = (json.dumps([dict(r) for r in transaction_data],
                            default=alchemyencoder))
        transaction_num = trans_offset + 1
    else:
        transaction_json = items["transaction_json"]
        transaction_num = items["transaction_num"]
        e = items["transaction_num"]
    transactions = json.loads(transaction_json)
    the_balance = '{:.2f}'.format(float(items["account_balance"]))
    # print(f"\t{items['account_name']} {the_balance}")
    the_title = title=('[aquamarine3]"' + items["account_name"] + ' ' + 
                       the_balance + '"[/]')
    table = Table(title=the_title)
    table.add_column("Number", style="bright_yellow")
    table.add_column("Date", style="aquamarine3")
    table.add_column("Transaction", style="bright_yellow", justify="right")
    table.add_column("Amount", justify="right", style="aquamarine3")
    table.add_column("Comment", style="bright_yellow")

    for transact in transactions:
        transact_amount = '{:.2f}'.format(float(transact["amount"]))
        transact_cdate = (datetime.datetime.strptime(transact["cdate"],
                          "%Y-%m-%d").strftime('%m/%d/%Y'))
        table.add_row(f'{e}', f'{transact_cdate}', f'{transact["action"]}', 
                      f'{transact_amount}', f'{transact["comment"]}')
        e = e + 1
    console = Console()
    console.print(table)
    items.update({"transaction_json": transaction_json, "transaction_num":
                  transaction_num})
    return items

def trans_act1a(items):
    print()
    okay_it = go_ahead("Make a " + items['action'])
    if okay_it == 'n':
        items.update({"menu_option": "menu"})
        return items
    else:
        items.update({"menu_option": "trans_act1b"})
        return items

def trans_act1b(items):
    print()
    trans_time = time.strftime('%m/%d/%Y')
    okay_it = go_ahead("Enter This Date: " + trans_time)
    if okay_it == 'y':
        items.update({"menu_option": "trans_act1d", "the_date": trans_time})
    else:
        items.update({"menu_option": "trans_act1c"})
    return items

def trans_act1c(items):
    print()
    print("Enter Date:\n")
    print()
    the_date = date_maker('month')
    print(the_date)
    okay_it = go_ahead("Is this okay? ")
    if okay_it == 'y':
        items.update({"menu_option": "trans_act1d", "the_date": the_date})
    else:
        items.update({"menu_option": "menu"})
    return items

def trans_act1d(items):
    print()
    print('enter amount for the ' + items["action"])
    amount = currency('y', items["action"])
    if items["action"] == "Withdraw":
        the_amount = float('-' + amount)
    else:
        the_amount = float(amount)
    the_amount_show = '{:.2f}'.format(the_amount)
#    trans_time = time.strftime('%m/%d/%Y')
#    items.update({"the_date": trans_time})
    new_transaction = (items["the_date"] + ' ' + items["action"] + ' ' +
                       the_amount_show)
    items.update({"transaction_item": new_transaction, 
                  "menu_option": "trans_act2", "amount": the_amount})
    return items

def trans_act2(items):
    print()
    print(items["transaction_item"])
    print()
    okay_it = go_ahead("if this is okay enter?")
    if okay_it == 'y':
        items.update({"menu_option": "trans_act3"})
        return items
    elif okay_it == 'n':
        items.update({"menu_option": "menu"})
        return items
    else:
        the_message = ('[bold red]Please enter either "y" or "n"![/]')
        items.update({"message_opt": "yes", "message": the_message})
        return items

def trans_act3(items):
    print()
    print(items["transaction_item"])
    print()
    add_comment = go_ahead('Add a comment to this transaction?')
    if add_comment == 'y':
        items.update({"menu_option": "trans_act4"}) 
        return items
    elif add_comment == 'n':
        rec_comment = 'no comment'
        the_amount_show = '{:.2f}'.format(items["amount"])
        new_transaction = (items["the_date"] + ' ' + items["action"] + ' ' +
                                the_amount_show + ' - ' + '\"' + 
                                rec_comment + '\"')
        items.update({"menu_option": "trans_act5", "the_comment": rec_comment,
                      "transaction_item": new_transaction})
        return items
    else:
        the_message = ('[bold red]Please enter either "y" or "n"![/]')
        items.update({"message_opt": "yes", "message": the_message})
        return items

def trans_act4(items):
    print()
    print(items["transaction_item"])
    print()
    rec_comment = input('Add comment: ')
    the_amount_show = '{:.2f}'.format(items["amount"])
    new_transaction = (items["the_date"] + ' ' + items["action"]
          + ' ' + the_amount_show + ' - \"' + rec_comment + '\"')
    items.update({"menu_option": "trans_act5", "the_comment": rec_comment,
                  "transaction_item": new_transaction})
    return items

def trans_act5(items):
    print()
    print(items["transaction_item"])
    print()
    record_it = go_ahead("Record this transaction?")
    if record_it == 'y':
        db_date = datetime.datetime.strptime(items["the_date"], '%m/%d/%Y')
        new_transaction = (Transaction(action=items["action"],
                           amount=items["amount"], cdate=db_date,
                           comment=items["the_comment"], account_id=items
                           ["selected_account"]))
        db_session.add(new_transaction)
        db_session.commit()
        new_balance = (Transaction.query.with_entities(func.sum(Transaction.
                       amount).filter(Transaction.account_id == items
                       ["selected_account"]).label('total')).first().total)
        the_account = Account.query.get(items["selected_account"])
        new_balance = round(new_balance, 2)
        the_account.balance = new_balance
        db_session.commit()
        transaction_len = items["transaction_len"] + 1
        items.update({"account_balance": new_balance, "data_load": "re-load",
                      "menu_option": "menu", "transaction_len": 
                      transaction_len})
        return items
    elif record_it == 'n':
        items.update({"menu_option": "menu"})
        return items
    else:
        the_message = ('[bold red]Please enter either "y" or "n"![/]')
        items.update({"message_opt": "yes", "message": the_message})
        return items


def select_transaction(items):
    if items["menu_option"] == 'select':
        if items["transaction_num"] + 4 <= items["transaction_len"]:
            list_end = 0
        else:
            list_end = items["transaction_len"] - (items["transaction_num"]
                                                   + 4)
        print()
        print('Select Transaction (' + str(items["transaction_num"]) + ' - ' +
              str(items["transaction_num"] + 4 + list_end) + ')')
        print('Return (r):')
        print()
        selected_transaction = input('Select: ')
        system('clear')
        if selected_transaction == 'r':
            items.update({"menu_option": "menu"})
            return items
        elif selected_transaction.isnumeric() is False:
            items.update({"message_opt": "yes", "message": '"Selection must\
                          be a \'number\'"'})
            return items
        elif int(selected_transaction) < items["transaction_num"] or \
                (int(selected_transaction) > (items["transaction_num"] + 4 +
                 list_end)):
            items.update({"message_opt": "yes", "message": '"Selection must \
                    be within \'number\' range"'})
            return items
        else:
            items.update({"menu_option": "selected", "selected_transaction":
                          selected_transaction})
            return items
    else:
        e = items["transaction_num"]
        transactions = json.loads(items["transaction_json"])

        for transact in transactions:
            transact_amount = '{:.2f}'.format(float(transact["amount"]))
            transact_cdate = (datetime.datetime.strptime(transact["cdate"],
                              "%Y-%m-%d").strftime('%m/%d/%Y'))
            row = ([e, f'{e}) {transact_cdate} {transact["action"]} {transact_amount} - \
"{transact["comment"]}"', transact["id"]])
            if row[0] == int(items["selected_transaction"]):
                break
            else:
                e = e + 1

        items.update({"menu_option": "edit_menu", "transaction_id": row[2],
                      "transaction_item": row[1]})
        return items
