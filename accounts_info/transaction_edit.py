from sqlalchemy import func
from os import system
from applets.applet import go_ahead, currency, transaction_list
from .models import Account, db_session, Transaction
from rich import print
from datetime import datetime


# Break up listed transaction
def transaction_spliter(transaction):
    transaction_split = transaction.split(' ')
    transaction_split2 = transaction.split(' - ')
    transaction_comment = transaction_split2[1]
    return transaction_split, transaction_comment


def date_maker(date_item):
    while date_item == 'month':
        date_month = input('\tMonth: ')
        if date_month.isdigit() is True and len(date_month) > 0 and \
                len(date_month) <= 2:
            date_month = date_month.zfill(2)
            print('\t' + date_month)
            date_item = 'day'
            pass
        else:
            print('[red]"Month should be two digits (numbers only)"[/red]')
            date_item = 'month'

    while date_item == 'day':
        date_day = input('\tDay: ')
        if date_day.isdigit() is True and len(date_day) > 0 and \
                len(date_day) <= 2:
            date_day = date_day.zfill(2)
            print('\t' + date_month + '/' + date_day)
            date_item = 'year'
            pass
        else:
            print('[red]"Day should be two digits (numbers only)"[/red]')
            date_item = 'day'

    while date_item == 'year':
        date_year = input('\tYear: ')
        if date_year.isdigit() is True and len(date_year) == 4:
            new_date = date_month + '/' + date_day + '/' + date_year
            return new_date
        else:
            print('[red]"Year should be four digits (numbers only)"[/red]')
            date_item = 'year'


def tedit_menu(items):
    print('Edit Menu')
    print('\n (1) Edit date\n'
          ' (2) Switch action (Deposit/Withdraw)\n'
          ' (3) Change Amount\n'
          ' (4) Edit Comment\n'
          ' (5) Delete Transaction\n'
          ' (6) Return')
    print()
    edit_it = input('Select: ')
    if edit_it.isdigit() is True and int(edit_it) >= 1 and \
            int(edit_it) <= 6:
        items.update({"menu_option": edit_it})     
        return items
    else:
        items.update({"menu_option": "edit_menu", "message_opt": "yes",
                      "message": "\"Your selection must be a \'number\' "
                      "between 1 and 6\""})
        return items


# Change Date
def edit_one(items):
    transaction_split, transaction_comment = (transaction_spliter(items
                                              ["transaction_item"]))
    the_transaction = Transaction.query.get(items["transaction_id"])
    date_cdate = (datetime.strptime(str(the_transaction.cdate),
                  "%Y-%m-%d").strftime('%m/%d/%Y'))
    date_edit = go_ahead(f'Change Date from {date_cdate}')
    if date_edit == 'y':
        print()
        new_date = date_maker('month')
        print(' ' + '\n' + 'New Date: ' + new_date)
        date_approve = go_ahead('Is this okay?')
        if date_approve == 'y':
            db_time = (datetime.strptime(new_date, '%m/%d/%Y'))
            the_transaction.cdate = db_time.date()
            db_session.commit()
            new_update = ('Update: ' + new_date + ' ' + 
                            the_transaction.action + ' ' + 
                            '{:,.2f}'.format(float(the_transaction.amount)) + 
                            ' - "' + the_transaction.comment + '"')
            if the_transaction.action == 'Transfer':
                transfer_transaction = Transaction.query.get(the_transaction.
                                       transfer_id)
                transfer_transaction.cdate = db_time.date()
                db_session.commit()
                transfer_update = ('Update: ' + new_date + ' ' +
                                   transfer_transaction.action + ' ' +
                                   '{:,.2f}'.format
                                   (float(transfer_transaction.amount)) + ' - "' +
                                   transfer_transaction.comment + '" \n'
                                   + new_update)
                items.update({"message_opt": "yes", "message": transfer_update,
                              "menu_option": "edit_menu", "data_load": 
                              "re-load"})
                return items
            else:
                items.update({"message_opt": "yes", "message": new_update, 
                              "menu_option": "edit_menu", "data_load": 
                              "re-load"})
            return items
        else:
            items.update({"menu_option": "edit_menu"})
            return items
    else:
        items.update({"menu_option": "edit_menu"})
        return items


# Change action
def edit_two(items):
    the_transaction = Transaction.query.get(items["transaction_id"])
    if the_transaction.action == "Transfer":
        items.update({"menu_option": "edit_menu", "message_opt": "yes",
                      "message": "[bold red]Only 'Deposits' and 'Withdraws'" 
                      " can be switched not 'Transfers'"})
        return items
    else:
        if the_transaction.action == 'Deposit':
            action_new = 'Withdraw'
        else:
            action_new = 'Deposit'
        action_switch = go_ahead('Change ' + the_transaction.action + 
                                 ' to ' + action_new)
        if action_switch == 'y':
            items.update({"menu_option": "2_show"})
            return items
        else:
            items.update({"menu_option": "edit_menu"})
            return items

def edit_two_show(items):
    the_transaction = Transaction.query.get(items["transaction_id"])
    the_account = Account.query.get(the_transaction.account_id)
    if the_transaction.action == 'Deposit':
        action_new = 'Withdraw'
        transaction_total = the_transaction.amount * 2
        dash = ''
        sign = '-'
    else:
        action_new = 'Deposit'
        transaction_total = the_transaction.amount * 2
        sign = ''
        dash = '-'
    date_cdate = (datetime.strptime(str(the_transaction.cdate),
              "%Y-%m-%d").strftime('%m/%d/%Y'))
    print('Original transaction: ' + str(date_cdate) + ' ' +
          the_transaction.action + ' ' + dash + '{:,.2f}'.format
          (the_transaction.amount).strip('-'))
    print('New transaction: ' + str(date_cdate) + ' ' + action_new + 
          ' ' + sign + '{:,.2f}'.format(the_transaction.amount)
          .strip('-'))

    transaction_show = ('{:,.2f}'.format(float(transaction_total))
                        .strip('-'))
    new_amount = (sign + '{:,.2f}'.format(the_transaction.amount).strip('-'))
    print()
    print('Alter balance: ' + sign + transaction_show)
    transaction_total = (sign + str(transaction_total).strip('-'))
    print()
    do_trans = go_ahead("Is this okay?")
    if do_trans == 'y':
        the_transaction.amount = new_amount
        the_transaction.action = action_new
        db_session.commit()
        new_balance = (Transaction.query.with_entities(func.sum
                       (Transaction.amount).filter
                       (Transaction.account_id == items
                        ["selected_account"]).label('total')).first().total)
        the_account.balance = new_balance
        db_session.commit()
        transaction_item = ('Updated: ' + str(date_cdate) + ' ' + 
                            action_new + ' ' + new_amount + ' - ' + 
                            the_transaction.comment)
        items.update({"transaction_item": transaction_item, 
                      "menu_option": "edit_menu", "data_load": 
                      "re-load", "account_balance": new_balance})
        return items
    else:
        items.update({"menu_option": "edit_menu"})
        return items


# Change amount
def edit_three(items):
    transaction_split, transaction_comment = (transaction_spliter(items
                                              ["transaction_item"]))

    the_transaction = Transaction.query.get(items["transaction_id"])
    
    present_amount = the_transaction.amount
    change_amt = go_ahead('Change amount of ' + the_transaction.action
                          + ' from ' + '{:,.2f}'.format(the_transaction.amount) + '? ')
    if change_amt == 'y':
        new_amount = currency('y', the_transaction.action)
        if the_transaction.action != 'Transfer':
            if the_transaction.action == "Withdraw":
                new_amount = float('-' + new_amount)
            else:
                new_amount = float(new_amount)
            new_amount_show = '{:,.2f}'.format(new_amount)
            new_transaction = (str(the_transaction.cdate) + ' ' + the_transaction.action
                               + ' ' + new_amount_show)
            print(new_transaction)
            do_it = go_ahead('Submit this new transaction?')
            if do_it == 'y':
                the_transaction.amount = new_amount
                db_session.commit()
                new_balance = (Transaction.query.with_entities(func.sum(Transaction.
                               amount).filter(Transaction.account_id == items
                               ["selected_account"]).label('total')).first().total)
                new_balance = round(new_balance, 2)
                new_balance_show = '{:,.2f}'.format(new_balance)
                the_account = Account.query.get(the_transaction.account_id)
                the_message = ('Updated ' + the_account.name + ' balance to ' +
                               new_balance_show + '\n')
                date_cdate = (datetime.strptime(str(the_transaction.cdate),
                              "%Y-%m-%d").strftime('%m/%d/%Y'))
                new_transaction_item = (date_cdate + ' ' + the_transaction.
                                        action + ' ' + new_amount_show + ' - "' 
                                        + the_transaction.comment + '"')
                items.update({"message_opt": "yes", "message": the_message, 
                              "data_load": "re-load", "menu_option": "edit_menu", 
                              "transaction_item": new_transaction_item,
                              "account_balance": new_balance}) 
                return items
            else:
                items.update({"menu_option": "edit_menu"})
                return items
        else:
            transfer_transaction = (Transaction.query.get
                                    (the_transaction.transfer_id))
            if the_transaction.amount < 0:
                the_amount = float('-' + new_amount)
                transfer_amount = float(new_amount)
            else:
                the_amount = float(new_amount)
                transfer_amount = float('-' + new_amount)
            print(the_amount)
            print(transfer_amount)
            # hello = input('hello')
            the_amount_show = '{:,.2f}'.format(the_amount)
            the_transaction.amount = the_amount
            transfer_transaction.amount = transfer_amount
            db_session.commit()
            transfer_balance = (Transaction.query.with_entities(func.sum(Transaction.
                                amount).filter(Transaction.account_id == 
                                transfer_transaction.account_id).label
                                ('total')).first().total)
            transfer_balance = round(transfer_balance, 2)
            transfer_balance_show = '{:,.2f}'.format(transfer_balance)
            transfer_account = (Account.query.get
                                (transfer_transaction.account_id))
            the_balance = (Transaction.query.with_entities(func.sum(Transaction.
                           amount).filter(Transaction.account_id == 
                           the_transaction.account_id).label('total')).first()
                           .total)
            the_balance = round(the_balance, 2)
            the_balance_show = '{:,.2f}'.format(the_balance)
            the_account = Account.query.get(the_transaction.account_id)
            the_message = ('Updated ' + the_account.name + ' balance to ' +
                           the_balance_show)
            date_cdate = (datetime.strptime(str(the_transaction.cdate),
                          "%Y-%m-%d").strftime('%m/%d/%Y'))
            new_transaction_item = (date_cdate + ' ' + the_transaction.action 
                                    + ' ' + the_amount_show + ' - "' + 
                                    the_transaction.comment + '"')
            transfer_message = ('Updated ' + transfer_account.name +
                                ' balance to ' + transfer_balance_show + '\n'
                                + the_message)
            items.update({"message_opt": "yes", "message": transfer_message, 
                          "data_load": "re-load", "menu_option": "edit_menu",
                          "transaction_item": new_transaction_item,
                          "account_balance": the_balance})
            return items
    else:
        items.update({"menu_option": "edit_menu"})
        return items


# Edit Commnent
def edit_four(items):
    transaction_split, transaction_comment = (transaction_spliter(items
                                              ["transaction_item"]))
    the_transaction = Transaction.query.get(items["transaction_id"])  
    comment_edit = go_ahead('Edit Comment ' + the_transaction.comment)
    if comment_edit == 'y':
        print()
        new_comment = input('New commnent: ')
        print('"' + new_comment + '"')
        comment_pass = go_ahead('Record this new comment?')
        if comment_pass == 'y':
            the_transaction.comment = new_comment
            db_session.commit()
            date_cdate = (datetime.strptime(str(the_transaction.cdate),
                          "%Y-%m-%d").strftime('%m/%d/%Y'))
            transaction_updated = ('Updated: ' + date_cdate + ' ' +
                                   the_transaction.action + ' ' +
                                   '{:,.2f}'.format(the_transaction.amount)
                                   + ' - "' + new_comment + '"')
            items.update({"menu_option": "edit_menu", "data_load": "re-load",
                          "transaction_item": transaction_updated})
            return items
        else:
            items.update({"menu_option": "edit_menu"})
            return items
    else:
        items.update({"menu_option": "edit_menu"})
        return items


# Delete transaction
def edit_five(items):
    transaction_split, transaction_comment = (transaction_spliter
                                              (items["transaction_item"]))

    the_transaction = Transaction.query.get(items["transaction_id"])
    the_account = Account.query.get(the_transaction.account_id)
    transaction_amount = the_transaction.amount
    transaction_amount_show = '{:.2f}'.format(float(transaction_amount))
    delete_pass = go_ahead('Delete selected transaction?')
    if delete_pass == 'y':
        del_transaction = Transaction.query.get(the_transaction.id)
        db_session.delete(del_transaction)
        db_session.commit()
        the_balance = (Transaction.query.with_entities
                       (func.sum(Transaction.amount).filter(Transaction.
                       account_id == the_transaction.account_id)
                       .label('total')).first().total)
        the_account.balance = the_balance
        db_session.commit()
        the_balance_show = '{:.2f}'.format(float(the_balance))
        delete_message_1 = ('\"New balance: ' + the_account.name + ' - '
                            + the_balance_show + '\"') 
        if the_transaction.action == 'Transfer':
            transfer_transaction = Transaction.query.get(the_transaction.
                                                         transfer_id)
            transfer_account = Account.query.get(transfer_transaction.account_id)
            db_session.delete(transfer_transaction)
            db_session.commit()
            transfer_balance = (Transaction.query.with_entities
                                (func.sum(Transaction.amount)
                                .filter(Transaction.account_id == 
                                transfer_transaction.account_id).
                                label('total')).first().total)
            transfer_account.balance = transfer_balance
            db_session.commit()
            # if not transfer_balance:
            #    transfer_balance = 0
            transfer_balance_show = '{:.2f}'.format(float(transfer_balance))
            message = ('\"New balance: ' + transfer_account.name + ' - '
                       + transfer_balance_show + '\"\n' + delete_message_1)
            transaction_len = items["transaction_len"] - 1
            print(the_balance)
            hello = input("hello")
            items.update({"menu_option": "edit_menu", "message_opt": "yes", 
                          "message": message, "data_load": "re-load", 
                          "transaction_len": transaction_len, 
                          "account_balance": the_balance})
            return items
        else:
            message = delete_message_1
            transaction_len = items["transaction_len"] - 1
            items.update({"menu_option": "edit_menu", "message_opt": "yes", \
                          "message": message, "data_load": "re-load", \
                          "transaction_len": transaction_len, 
                          "account_balance": the_balance})
        return items
    else: 
        items.update({"menu_option": "menu_edit"})
        return items     
    
