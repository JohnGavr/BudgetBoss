#!/usr/bin/env python3

import json
import os
from datetime import datetime,date

import mysql.connector
from prettytable import PrettyTable

revenue_categories = ["Salary", "Others"]
expense_categories = ["Going Out", "Smoking", "Vehicles & Gas", "Shopping", "SuperMarket", "Other"]

### Connect to mysql server
def connect_to_mysql(host, user, password, database=None, print_messages=True):
    '''Function for connecting to mysql'''
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
        )

        if connection.is_connected() and print_messages:
            print(f"Connected to MySQL database '{database}'")
        return connection
    except mysql.connector.Error as mistake:
        print(f"Error: {mistake}")
        return None
    
def insert_statement(table,day_input, value_input, category_input, comments_input):
    ''' Function for Insert Statement'''
    statement = f"INSERT INTO `{table}` (`date`, `value`, `category`, `comments`) VALUES ('{day_input}', '{value_input}', '{category_input}', '{comments_input}')"
    return statement
    
### Add Menu

def display_menu():
    ''' Basic Menu'''
    print("Menu:")
    print("1. Add Revenue")
    print("2. Add Expense")
    print("3. Reports")
    print("4. Quit")

def submenu():
    ''' Second Menu'''
    print("1. Total Revenues")
    print("2. Total Expenses")
    print("3. PnL")
    print("4. Back to Main Menu")

def configuration_file():
    ''' Function for user to see the configuration file and manage it'''
    print("Configuration File")
    ### Save Variables as localhost,user,password,database name into a JSON file.

def kind_date(report):
    '''Date of the transaction'''
    while True:
        # Insert Date
        if report == 0 :
            date_input = input("Enter a date (DD-MM-YYYY): ")
        elif report == 1 :
            date_input = input("Enter a date from (DD-MM-YYYY): ")
        elif report == 2 :
            date_input = input("Enter a date to (DD-MM-YYYY):")
        # Convert the string to a datetime object
        if report == 2 and not date_input:
            date_input = date.today().strftime("%d-%m-%Y")
        try:
            date_input = datetime.strptime(date_input, "%d-%m-%Y")
            formatted_date= date_input.strftime('%Y-%m-%d')
            return date_input
            break
        except ValueError:
            print("Invalid date format. Please enter the date in DD-MM-YYYY format.")

               
def kind_value():
    ''' Value of transaction'''
    while True:
        # Insert Decimal number
        decimal_input = input("Please enter a decimal number: ")
        try:
            value_input=float(decimal_input)
            print(f"You entered: {value_input}")
            return value_input
        except ValueError:
            # Handle the case where the user didn't enter a valid decimal number
            print("Invalid input. Please enter a valid decimal number.")

def kind_category(category_options):
    '''Category of transaction'''
    while True:
        try:
            print("Category Options:")
            for i, category in enumerate(category_options, start=1):
                print(f"{i}. {category}")
                
            category_input= int(input("Enter the category number: "))
            if 1 <= category_input <= len(category_options):
                return category_input
            else:
                print("Invalid input. Please enter a valid category number.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def kind_comments():
    ''' Comments of transacion'''
    comments_input = input("Enter comments: ")
    return comments_input
    
    
def add_revenue():
    ''' Function which take insert statement for revenue'''
    sql_connect= connect_to_mysql(sql_host,sql_user,sql_password,sql_database,print_messages=False)
    sql_cursor= sql_connect.cursor()
    print("Add Revenue")
    date_input= kind_date(0)
    value_input = kind_value()
    category_input = kind_category(revenue_categories)
    comments_input = kind_comments()
    sql = insert_statement("revenue",date_input,value_input, category_input, comments_input)
    sql_cursor.execute(sql)
    sql_connect.commit()
    sql_connect.close()
    sql_cursor.close()

def add_expense():
    ''' Function which take insert statement for expense '''
    sql_connect = connect_to_mysql(sql_host, sql_user, sql_password, sql_database, print_messages=False)
    sql_cursor = sql_connect.cursor()
    print("Add Expense")
    date_input = kind_date(0)
    value_input = kind_value()
    category_input = kind_category(expense_categories)
    comments_input = kind_comments()
    sql = insert_statement("expense", date_input, value_input, category_input, comments_input)
    sql_cursor.execute(sql)
    sql_connect.commit()
    sql_connect.close()
    sql_cursor.close()

def sum_reports(table,tag,date_from,date_to):
    ''' Reports function'''
    sql_connect= connect_to_mysql(sql_host,sql_user,sql_password,sql_database,print_messages=False)
    sql_cursor= sql_connect.cursor()
    ### Add SUM statement
    rev_query= f"SELECT SUM(value) FROM {table} WHERE date >= '{date_from}' and date <='{date_to}'"
    sql_cursor.execute(rev_query)
    total_rev= sql_cursor.fetchone()

    if tag is not None:
        print(f"Total {tag} are : {total_rev[0]}")

    exp_query= f"SELECT SUM(value) FROM (database)"
    #sql_cursor.execute(exp_query)
    #total_exp= sql_cursor.fetchone()
    #print(f"Total Expenses are : {total_exp[0]}")
    sql_connect.close()
    sql_cursor.close()
    return total_rev[0]

def pnl():
    ''' Reports function'''
    date_from=kind_date(1)
    date_to=kind_date(2)
    total_revs= sum_reports('revenue',None,date_from,date_to)
    total_exps= sum_reports('expense',None,date_from,date_to)
    if total_revs is None:
        total_revs=0
    elif total_exps is None:
        total_exps=0
    total_pnl= total_revs - total_exps
    print(f"Total Profit and loss: {total_pnl}")

def execute_select_all(table_name):
    ''' Reports function'''
    sql_connect= connect_to_mysql(sql_host,sql_user,sql_password,sql_database,print_messages=False)
    sql_cursor= sql_connect.cursor()
    date_from=kind_date(1)
    date_to=kind_date(2)
     # Execute the SELECT query
    query = f"SELECT * FROM {table_name} WHERE date >= '{date_from}' and date <='{date_to}' UNION ALL SELECT 'Total', SUM(value),'','' FROM {table_name} WHERE date >= '{date_from}' and date <='{date_to}' ORDER BY date"
    sql_cursor.execute(query)
    # Fetch all rows
    rows = sql_cursor.fetchall()
    table = PrettyTable()
    columns= [desc[0] for desc in sql_cursor.description]
    table.field_names = columns
    for row in rows:
        table.add_row(row)
    print(table)
    sql_connect.close()
    sql_cursor.close()

### Save Variables as localhost,user,password,database name into a JSON file.
if os.path.exists('variables.json'):
    print("The file exists")
    # Read variables from the JSON file
    loaded_data = None

    try:
        with open('variables.json', 'r', encoding='utf-8') as json_file:
            loaded_data = json.load(json_file)
    except FileNotFoundError:
        print("File not found. Run the script to create the file first.")

    # Print read variables
    if loaded_data:
        sql_host= loaded_data["host"]
        sql_user= loaded_data["user"]
        sql_password= loaded_data["password"]
        sql_database= loaded_data["database"]
        print(f"You are going to connect to {sql_user}@{sql_host} and your password is {sql_password}\nand the database name is {sql_database}")
else:
    usr_input1= input('Enter the host(localhost): ')
    usr_input2= input('Enter the user of mysql: ')
    usr_input3= input('Enter the password of user: ')
    usr_input4= input('Enter the database name you want to create: ')

    with open('variables.json', 'w', encoding='utf-8') as json_file:
        data = {
            "host": usr_input1,
            "user": usr_input2,
            "password": usr_input3,
            "database": usr_input4
        }
        json.dump(data, json_file)

    try:
        with open('variables.json', 'r', encoding='utf-8') as json_file:
            loaded_data = json.load(json_file)
    except FileNotFoundError:
        print("File not found. Run the script to create the file first.")

    # Print read variables
    if loaded_data:
        sql_host= loaded_data["host"]
        sql_user= loaded_data["user"]
        sql_password= loaded_data["password"]
        sql_database= loaded_data["database"]
        print(f"You are going to connect to {sql_user}@{sql_host} and your password is {sql_password}\nand the database name is {sql_database}")

## Connect to SQL to create databases        
sql_connect= connect_to_mysql(sql_host,sql_user,sql_password)
sql_cursor= sql_connect.cursor()

# Create Database
try:
    sql_cursor.execute(f"CREATE DATABASE {sql_database}")
    print(f"Database {sql_database}, created successfully!")
except mysql.connector.Error as err:
    print(f"Database {sql_database} exists. We continue.")

##Close Connection
sql_connect.close()
sql_cursor.close()

### Create Tables
## Connect to SQL Database
sql_connect= connect_to_mysql(sql_host,sql_user,sql_password,sql_database)
sql_cursor= sql_connect.cursor()

try:
    # Category Options: 1. Salary 2. Others
    sql_cursor.execute("CREATE TABLE revenue (date DATE, value DECIMAL(10, 2), category INT CHECK (category BETWEEN 1 AND 2), comments VARCHAR(255))")
    
    # Category Options: 1. Going Out 2. Vehicles & Gas 3. Shopping 4. SuperMarket 5. Other
    sql_cursor.execute("CREATE TABLE expense (date DATE, value DECIMAL(10, 2), category INT CHECK (category BETWEEN 1 AND 5), comments VARCHAR(255))")
    
    print("Database revenue and expense, created succesfully!")
except mysql.connector.Error as err:
    print(f"The table exist, we continue.")

while True:
    display_menu()
    # Get user input
    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        add_revenue()
    elif choice == '2':
        add_expense()
    elif choice == '3':
        submenu_choice = None
        while submenu_choice != '4':
            submenu()
            submenu_choice = input("Enter your submenu choice: ")
            if submenu_choice == '1':
                execute_select_all('revenue')
            elif submenu_choice == '2':
                execute_select_all('expense')
            elif submenu_choice == '3':
                pnl()
            elif submenu_choice =='4':
                print("Returning to main menu")
            else:
                print("Invalid choice. Please try again")
    elif choice == '4':    
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 3.")
