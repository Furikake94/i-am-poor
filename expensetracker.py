import sqlite3, tkinter, sys
from datetime import datetime


conn = sqlite3.connect('expenses.sqlite')
cur = conn.cursor()
sql = '''create table if not exists Expenses (
                id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                Amount INTEGER,
                Category TEXT,
                Details TEXT,
                Date TEXT
                );
            create table if not exists Income (
                id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                Amount INTEGER,
                Category TEXT,
                Details TEXT,
                Date TEXT
                )
        '''
cur.executescript(sql)
conn.commit()
conn.close()
#this dictionary allows the user to input 'e' and 'i'
#instead of 'expenses' and 'income'
table_dict = {  'expenses' : 'expenses',
                'e' : 'expenses',
                'income' : 'income',
                'i' : 'income'
            }


def logAmount():
    '''
    logs the expense/income in the database.
    Amount = number
    Category = text
    Details = text or blank
    table = text
    '''
    start = 1
    #this loop allows the program to restart
    while True:
            if start != 1:
                restart = input('Restart? [Y/N]')
                if restart.lower() == 'y':
                    pass
                elif restart.lower() == 'n':
                    break
                else:
                    print('Invalid input: must type either Y or N')
                    continue
            tries = 10
            attempt = 0

            #this part makes sure that the script can't be stuck in a loop while picking
            #arguments
            for attempt in range(tries):
                if attempt == (tries-1):
                    sys.exit('Maximum amount of attempts reached. The program will terminate.')

                else:
                    try:
                        Amount = int(input('Select the Amount: '))
                        if Amount < 0:
                            attempt += attempt
                            print('The number must be positive')
                        else:
                            attempt = 0
                            break
                    except ValueError:
                        print('Error: You must pick a number as an amount')
                        attempt += attempt


            for attempt in range(tries):
                if attempt == (tries-1):
                    sys.exit('Maximum amount of attempts reached. The program will terminate.')
                else:
                    Category = input('Add the category: ')
                    if Category == '':
                        print('Error. You must select a category')
                        attempt += attempt

                    else:
                        attempt = 0
                        break

            Details = input('Add details or leave blank: ')
            Date = str(datetime.now())
            data = (Amount, Category, Details, Date)

            for attempt in range(tries):
                if attempt == (tries-1):
                    sys.exit('Maximum amount of attempts reached. The program will terminate.')

                else:
                    table_input = input('Type [e]xpenses or [i]ncome to see the logs: ')
                    if table_input.lower() not in ['income', 'expenses', 'e', 'i']:
                        print("Not an appropriate choice. You must type either expenses or income")
                        attempt += attempt
                    else:
                        attempt = 0
                        break
            table = table_dict[table_input]
            conn = sqlite3.connect('expenses.sqlite')
            c = conn.cursor()
            sql = "INSERT INTO "+table+" VALUES (NULL, ?, ?, ?, ?)"
            c.execute(sql, data)
            conn.commit()
            conn.close()
            print('Amount logged successfully')
            if start == 1:
                start = 0





def view(category=None):
    '''
    Returns a list of all expenditure incurred, and the total expense,
    or all incomes generated and the total income.
    If a category is specified, it only returns info from that
    category
    '''

    tries = 10
    attempt = 0

    start = 1
    #this loop allows the program to restart
    while True:
        if start != 1:
            restart = input('Restart? [Y/N]')
            if restart.lower() == 'y':
                pass
            elif restart.lower() == 'n':
                break
            else:
                print('Invalid input: must type either Y or N')
                continue
        #this part makes sure that the script can't be stuck in a loop while picking
        #arguments
        for attempt in range(tries):

            if  attempt == (tries-1):
                print('Maximum amount of attempts reached. The program will terminate.')
                sys.exit(0)
            else:
                while True:
                    table_input = input('Type [e]xpenses or [i]ncome to see the logs: ')
                    if table_input.lower() not in ['income', 'expenses', 'e', 'i']:
                        attempt += attempt
                        print("Not an appropriate choice. You must type either expenses or income")
                    else:
                        attempt = 0
                        break

            table = table_dict[table_input]
            conn = sqlite3.connect('expenses.sqlite')
            c = conn.cursor()
            if category:
                sql = '''
                SELECT * FROM '''+table+''' WHERE category = '{}'
                '''.format(category)
                sql2 = '''
                SELECT sum(amount) FROM '''+table+''' WHERE category = '{}'
                '''.format(category)
            else:
                sql = '''
                SELECT * FROM '''+table+'''
                '''
                sql2 = '''
                SELECT sum(amount) FROM '''+table+'''
                '''
            c.execute(sql)
            resultsExp = c.fetchall()
            c.execute(sql2)
            total_amountExp = c.fetchone()[0]
            conn.close()
            print(total_amountExp, resultsExp)
            attempt = 0
            break
        if start == 1:
            start = 0


def delAmount():
    '''Deletes the selected line from
    the Expenses or Income table
    '''

    start = 1
    #this loop allows the program to restart
    while True:
        if start != 1:
            restart = input('Restart? [Y/N]')
            if restart.lower() == 'y':
                pass
            elif restart.lower() == 'n':
                break
            else:
                print('Invalid input: must type either Y or N')
                continue

        #this part makes sure that the script can't be stuck in a loop while picking
        #table and line to delete
        tries = 10
        attempt = 0
        for attempt in range(tries):

            if  attempt == (tries-1):
                print('Maximum amount of attempts reached. The program will terminate.')
                sys.exit(0)
            else:
                #lets the user pick the table in which to operate
                table_input = input('Type [e]xpenses or [i]ncome to see the logs: ')
                if  table_input.lower() not in ['income', 'expenses', 'e', 'i']:
                        print("Not an appropriate choice. You must type either expenses or income")
                        attempt += attempt
                else:
                        attempt = 0
                        break

        for attempt in range(tries):
            if attempt == (tries-1):
                sys.exit('Maximum amount of attempts reached. The program will terminate.')

            else:
                try:
                    #lets the user pick the item to delete
                    delid = int(input('type the idnumber of the line you wish to delete: '))
                    attempt = 0
                    break

                except ValueError:
                    print('Error: the id selected is not a number.')
                    attempt += attempt


        #this part deletes the line selected by the user. Table and delid are both
        #user-prompted choices
        table = table_dict[table_input]
        conn = sqlite3.connect('expenses.sqlite')
        c = conn.cursor()
        sql = '''DELETE FROM '''+table+''' WHERE id=?'''
        c.execute(sql, (delid, ))
        conn.commit()
        conn.close()
        print('Amount deleted successfully')
        if start == 1:
            start = 0


view()
