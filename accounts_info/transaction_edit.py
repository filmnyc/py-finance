from sqlalchemy import func
from os import system
from applets.applet import go_ahead, currency, transaction_list
from .models import Account, db_session, Transaction


# Break up listed transaction
def transaction_spliter(transaction):
    transaction_split = transaction.split(' ')
    transaction_split2 = transaction.split(' - ')
    transaction_comment = transaction_split2[1]
    return transaction_split, transaction_comment


def date_maker(date_item):
    while date_item == 'month':
        date_month = input('Month: ')
        if date_month.isdigit() is True and len(date_month) > 0 and \
                len(date_month) <= 2:
            date_month = date_month.zfill(2)
            # date_new = date_month + '/'
            print(date_month)
            date_item = 'day'
            pass
        else:
            print('"Month should be two digits (numbers only)"')
            date_item = 'month'

    while date_item == 'day':
        date_day = input('Day: ')
        if date_day.isdigit() is True and len(date_day) > 0 and \
                len(date_day) <= 2:
            date_day = date_day.zfill(2)
            # date_new = date_month + '/'
            print(date_month + '/' + date_day)
            date_item = 'year'
            pass
        else:
            print('"Day should be two digits (numbers only)"')
            date_item = 'day'

    while date_item == 'year':
        date_year = input('Year: ')
        if date_year.isdigit() is True and len(date_year) == 4:
            new_date = date_month + '/' + date_day + '/' + date_year
            return new_date
        else:
            print('"Day should be four digits (numbers only)"')
            date_item = 'year'


def tedit_menu(items):
    show = 'y'
    while show == 'y':
        print('Edit Menu')
        print('\n (1) Edit date\n'
              ' (2) Edit action\n'
              ' (3) Change Amount\n'
              ' (4) Edit Comment\n'
              ' (5) Delete Transaction\n'
              ' (6) Return')
        print()
        edit_it = input('Select: ')
        if edit_it.isdigit() is True and int(edit_it) >= 1 and \
                int(edit_it) <= 6:
            return edit_it
        else:
            system('clear')
            transaction_list(items)
            print()
            print(items["transaction_item"])
            print()
            print("\"Your selection must be a \'number\' between 1 and 6\"")


# Change Date
def edit_one(items):
    transaction_split, transaction_comment = (transaction_spliter(items
                                              ["transaction_item"]))
    date_edit = go_ahead('Change Date from ' + transaction_split[1])
    if date_edit == 'y':
        print()
        new_date = date_maker('month')
        print('New date: ' + new_date)
        date_approve = go_ahead('Is this okay?')
        if date_approve == 'y':
            date_new = new_date
            date_db = (db_session.query(Transaction).filter_by(id=items
                       ["transaction_id"]).first())
            date_db.cdate = date_new
            db_session.commit()
            transaction_updated = ('Updated: ' + new_date + ' ' +
                                   transaction_split[2] + ' ' +
                                   transaction_split[3] + ' - ' +
                                   transaction_comment)
            return transaction_updated
        else:
            return 're-edit'
    else:
        return 're-edit'


# Change action
def edit_two(items):
    transaction_split, transaction_comment = (transaction_spliter(items
                                              ["transaction_item"]))
    if transaction_split[2] == 'Deposit':
        action_new = 'Withdraw'
    else:
        action_new = 'Deposit'
    action_switch = go_ahead('Change ' + transaction_split[2] + ' to ' +
                             action_new)
    if action_switch == 'y':
        if action_new == 'Deposit':
            transaction_total = float(transaction_split[3].strip('$, -')) * 2
            sign = '+'
        else:
            action_new == 'Withdraw'
            transaction_total = float(transaction_split[3].strip('$')) * 2
            sign = '-'

        # Compare old transaction to new transaction
        if action_new == 'Withdraw':
            dash = '-'
        else:
            dash = '+'
        print('Original transaction: ' + transaction_split[1] + ' ' +
              transaction_split[2] + ' - ' + transaction_split[3])
        print('New transaction: ' + transaction_split[1] + ' ' + action_new +
              ' - ' + dash + transaction_split[3].strip('-'))

        transaction_show = '{:,.2f}'.format(float(transaction_total))

        # Alter balance
        print('Alter balance: ' + sign + transaction_show)
        transaction_total = (sign + str(transaction_total))
        do_trans = go_ahead("Is this okay?")
        if do_trans == 'y':

            # show old and new balance
            old_balance = (Transaction.query.with_entities(func.sum
                           (Transaction.amount).filter
                           (Transaction.account_id == items
                            ["selected_account"]).label('total')).first().
                           total)
            new_balance = str(float(old_balance) + float(transaction_total))
            new_balance_show = '{:.2f}'.format(float(new_balance))
            old_balance_show = '{:.2f}'.format(float(old_balance))
            print('Previous account balance: ' + old_balance_show + ' New account balance: \
' + new_balance_show)
            do_bal = go_ahead("Record this transaction? ")
            if do_bal == 'y':
                action_db = (db_session.query(Transaction).filter_by
                             (id=items["transaction_id"]).first())
                if action_new == 'Withdraw':
                    action_db.amount = '-' + transaction_split[3].strip('$')
                else:
                    action_db.amount = transaction_split[3].strip('$, -')

                action_db.action = action_new
                db_session.commit()
                balance_db = (db_session.query(Account).join(Transaction,
                              Transaction.account_id == Account.id,
                              isouter=True).filter(Transaction.id == items
                              ["transaction_id"]).first())
                balance_db.balance = new_balance
                db_session.commit()
                transaction_updated = ('Updated: ' + transaction_split[1]
                                       + ' ' + action_new + ' ' + dash +
                                       transaction_split[3].strip('-')
                                       + ' - ' + transaction_comment)
                return transaction_updated, new_balance
            else:
                system('clear')
                return 're-edit', 're-edit'
        else:
            system('clear')
            return 're-edit', 're-edit'
    else:
        system('clear')
        return 're-edit', 're-edit'


# Change amount
def edit_three(items):
    transaction_split, transaction_comment = (transaction_spliter(items
                                              ["transaction_item"]))
    present_amount = transaction_split[3].strip('$')
    change_amt = go_ahead('Change amount of ' + transaction_split[2]
                          + ' from ' + present_amount + '? ')
    if change_amt == 'y':
        new_amount = currency('y')
    else:
        system('clear')
        return 're-edit', 're-edit'
    if transaction_split[2] == 'Withdraw':
        new_amount_show = '-{:,.2f}'.format(float(new_amount))
    else:
        new_amount_show = '{:,.2f}'.format(float(new_amount))

    new_transaction = (transaction_split[1] + ' ' + transaction_split[2]
                       + ' - ' + new_amount_show)
    print(new_transaction)
    present_amount = present_amount.strip('-')
    do_it = go_ahead('Submit this new transaction?')
    if do_it == 'y':
        if transaction_split[2] == ('Deposit' and float(present_amount) >
                                    float(new_amount)):
            transaction_total = float(present_amount) - float(new_amount)
            sign = '-'
        elif transaction_split[2] == ('Withdraw' and float(present_amount) >
                                      float(new_amount)):
            transaction_total = float(present_amount) - float(new_amount)
            sign = '+'
        elif transaction_split[2] == ('Deposit' and float(new_amount) >
                                      float(present_amount)):
            transaction_total = float(new_amount) - float(present_amount)
            sign = '+'
        else:
            transaction_split[2] == ('Withdraw' and float(new_amount) >
                                     float(present_amount))
            transaction_total = float(new_amount) - float(present_amount)
            sign = '-'
    else:
        system('clear')
        return 're-edit', 're-edit'

    # Compare old transaction to new transaction
    print('Original transaction: ' + transaction_split[1] + ' ' +
          transaction_split[2] + ' - ' + present_amount)
    print('New transaction: ' + transaction_split[1] + ' ' +
          transaction_split[2] + ' - ' + new_amount_show)

    transaction_show = '{:,.2f}'.format(float(transaction_total))

    # Alter balance
    print('Alter balance: ' + sign + transaction_show)
    transaction_total = (sign + str(transaction_total))
    do_trans = go_ahead("If this is okay enter 'y'")
    if do_trans == 'y':
        pass
    else:
        system('clear')
        return 're-edit', 're-edit'

        # show old and new balance
    old_balance = (Transaction.query.with_entities(func.sum(Transaction.
                   amount).filter(Transaction.account_id == items
                   ["selected_account"]).label('total')).first().total)
    old_balance_show = '{:.2f}'.format(float(old_balance))
    new_balance = str(float(old_balance) + float(transaction_total))
    new_balance_show = '{:.2f}'.format(float(new_balance))
    print('Previous balance: ' + old_balance_show + ' New balance: '
          + new_balance_show)
    do_bal = go_ahead("Record this transaction?:")
    if do_bal == 'y':
        amount_db = (db_session.query(Transaction).filter_by(id=items
                     ["transaction_id"]).first())
        if transaction_split[2] == 'Withdraw':
            amount_db.amount = '-' + str(new_amount)
        else:
            amount_db.amount = new_amount
        db_session.commit()
        balance_db = (db_session.query(Account).join(Transaction, Transaction.
                      account_id == Account.id, isouter=True).
                      filter(Transaction.id == items["transaction_id"]).
                      first())
        balance_db.balance = new_balance
        db_session.commit()
        transaction_updated = ('Updated: ' + transaction_split[1] + ' ' +
                               transaction_split[2] + ' ' + new_amount_show +
                               ' - ' + transaction_comment)
        return transaction_updated, new_balance
    else:
        return 're-edit', 're-edit'


# Edit Commnent
def edit_four(items):
    transaction_split, transaction_comment = (transaction_spliter(items
                                              ["transaction_item"]))
    comment_edit = go_ahead('Edit Comment ' + transaction_comment)
    if comment_edit == 'y':
        print()
        new_comment = input('New commnent: ')
        print('"' + new_comment + '"')
        comment_pass = go_ahead('Record this new comment?')
        if comment_pass == 'y':
            comment_db = (db_session.query(Transaction).filter_by(id=items
                          ["transaction_id"]).first())
            comment_db.comment = new_comment
            db_session.commit()
            transaction_updated = ('Updated: ' + transaction_split[1] + ' ' +
                                   transaction_split[2] + ' ' +
                                   transaction_split[3] + ' - "' +
                                   new_comment + '"')
            return transaction_updated
        else:
            return 're-edit'
    else:
        return 're-edit'


# Delete transaction
def edit_five(items):
    transaction_split, transaction_comment = (transaction_spliter
                                              (items["transaction_item"]))

    the_transaction = Transaction.query.get(items["transaction_id"])
    the_account = Account.query.get(the_transaction.account_id)
    the_balance = (Transaction.query.with_entities(func.sum(Transaction.amount)
               .filter(Transaction.account_id == the_transaction.account_id)
               .label('total')).first().total)
    the_balance_show = '{:.2f}'.format(float(the_balance))
    transaction_amount = the_transaction.amount
    transaction_amount_show = '{:.2f}'.format(float(transaction_amount))
    delete_pass = go_ahead('Delete selected transaction?')
    if delete_pass == 'y':
        change_balance = -(the_transaction.amount) + the_balance
        change_balance_show = '{:.2f}'.format(float(change_balance))
        the_account.balance = change_balance
        db_session.commit()
        del_transaction = Transaction.query.get(the_transaction.id)
        db_session.delete(del_transaction)
        # db_session.commit()
        delete_message_1 = ('\"New balance: ' + the_account.name + ' - '
                            + change_balance_show + '\"') 
        if the_transaction.action == 'Transfer':
            transaction_to = Transaction.query.get(the_transaction.transfer_id)
            db_session.delete(transaction_to)
            account_to = Account.query.get(transaction_to.account_id)
            old_balance_to = (Transaction.query.with_entities(func.sum(Transaction.amount)
                       .filter(Transaction.account_id == transaction_to.account_id)
                       .label('total')).first().total)
            change_to_balance = -(transaction_to.amount) + old_balance_to
            change_to_balance_show = '{:.2f}'.format(float(change_to_balance))
            account_to.balance = change_to_balance
#            print(change_balance_show)
#            print(change_to_balance_show)
#            hello = input('hello')
            db_session.commit()
            message = ('\"New balance: ' + account_to.name + ' - '
                       + change_to_balance_show + '\"\n' + delete_message_1)
            transaction_len = items["transaction_len"] - 1
            items.update({"menu_option": "6", "message_opt": "yes", \
                          "message": message, "data_load": "re-load", \
                          "transaction_len": transaction_len, "account_balance":
                          change_balance})
        else:
            message = delete_message_1
            transaction_len = items["transaction_len"] - 1
            items.update({"menu_option": "6", "message_opt": "yes", \
                          "message": message, "data_load": "re-load", \
                          "transaction_len": transaction_len})
        return items
    else: 
        items.update({"menu_option": "menu_edit"})
        return items     
    
