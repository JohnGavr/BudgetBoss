#!/usr/bin/env python3

import json,os
import mysql.connector
from datetime import datetime

### Connect to mysql server
def connect_to_mysql(host, user, password, database=None, print_messages=True):
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if connection.is_connected() and print_messages:
            print(f"Connected to MySQL database '{database}'")
        return connection

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    
def insert_statement(table,decimal,day):
    sql = f"INSERT INTO `{table}` (`value`, `date`) VALUES ({decimal}, '{day}')"
    return sql
    
### Add Menu

def display_menu():
    print("Menu:")
    print("1. Add Revenue")
    print("2. Add Expense")
    print("3. Reports")
    print("4. Quit")

def submenu():
    print("1. Total Revenues")
    print("2. Total Expenses")
    print("3. PnL")
    print("4. Back to Main Menu")

def configuration_file():
    print("Configuration File")
    ### Save Variables as localhost,user,password,database name into a JSON file.

def kind_date():
    while True:
        # Insert Date
        date_input_str = input("Enter a date (YYYY-MM-DD): ")
        # Convert the string to a datetime object
        try:
            date_input = datetime.strptime(date_input_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use the format YYYY-MM-DD.")
        return date_input_str
        
def kind_number():        
    # Insert Decimal number
    user_input = input("Please enter a decimal number: ")
    try:
        decimal_number=float(user_input)
        print(f"You entered: {decimal_number}")
        return decimal_number
    except ValueError:
        # Handle the case where the user didn't enter a valid decimal number
        print("Invalid input. Please enter a valid decimal number.")
    
def add_revenue():
    sql_connect= connect_to_mysql(sql_host,sql_user,sql_password,sql_database,print_messages=False)
    sql_cursor= sql_connect.cursor()
    print("Add Revenue")
    date_input_str= kind_date()
    decimal_number = kind_number()
    sql = insert_statement("revenue",decimal_number,date_input_str)
    sql_cursor.execute(sql)
    sql_connect.commit()
    sql_connect.close()
    sql_cursor.close()

def add_expense():
    sql_connect= connect_to_mysql(sql_host,sql_user,sql_password,sql_database,print_messages=False)
    sql_cursor= sql_connect.cursor()
    print("Add Expense")
    date_input_str=kind_date()
    decimal_number=kind_number()
    sql = insert_statement("expense",decimal_number,date_input_str)
    sql_cursor.execute(sql)
    sql_connect.commit()
    sql_connect.close()
    sql_cursor.close()

def sum_reports(table,tag):
    sql_connect= connect_to_mysql(sql_host,sql_user,sql_password,sql_database,print_messages=False)
    sql_cursor= sql_connect.cursor()
    ### Add SUM statement
    rev_query= f"SELECT SUM(value) FROM {table}"
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
    total_revs= sum_reports('revenue',None)
    total_exps= sum_reports('expense',None)
    total_pnl= total_revs - total_exps
    print(f"Total Profit and loss; {total_pnl}")
    

### Save Variables as localhost,user,password,database name into a JSON file.
if os.path.exists('variables.json'):
    print("The file exists")
    # Read variables from the JSON file
    read_data = None

    try:
        with open('variables.json', 'r') as json_file:
            read_data = json.load(json_file)
    except FileNotFoundError:
        print("File not found. Run the script to create the file first.")

    # Print read variables
    if read_data:
        sql_host= read_data["host"]
        sql_user= read_data["user"]
        sql_password= read_data["password"]
        sql_database= read_data["database"]
        print(f"You are going to connect to {sql_user}@{sql_host} and your password is {sql_password}\nand the database name is {sql_database}")
else:
    usr_input1= input('Enter the host(localhost): ')
    usr_input2= input('Enter the user of mysql: ')
    usr_input3= input('Enter the password of user: ')
    usr_input4= input('Enter the database name you want to create: ')

    with open('variables.json', 'w') as json_file:
        data = {
            "host": usr_input1,
            "user": usr_input2,
            "password": usr_input3,
            "database": usr_input4
        }
        json.dump(data, json_file)

    try:
        with open('variables.json', 'r') as json_file:
            read_data = json.load(json_file)
    except FileNotFoundError:
        print("File not found. Run the script to create the file first.")

    # Print read variables
    if read_data:
        sql_host= read_data["host"]
        sql_user= read_data["user"]
        sql_password= read_data["password"]
        sql_database= read_data["database"]
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
    sql_cursor.execute("CREATE TABLE revenue (id INT AUTO_INCREMENT PRIMARY KEY, value DECIMAL(10. 2), date DATE)")
    sql_cursor.execute("CREATE TABLE expense (id INT AUTO_INCREMENT PRIMARY KEY, value DECIMAL(10, 2), date DATE)")
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
                sum_reports('revenue','Revenues')
            elif submenu_choice == '2':
                sum_reports('expense', 'Expenses')
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
