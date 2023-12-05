#!/usr/bin/env python3

import json,os
import mysql.connector
from datetime import datetime

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

### Connect to mysql server

def connect_to_mysql(host, user, password, database=None):
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if connection.is_connected():
            print(f"Connected to MySQL database '{database}'")
            return connection

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

sql_connect= connect_to_mysql(sql_host,sql_user,sql_password)

sql_cursor= sql_connect.cursor()

# Create Database
try:
    sql_cursor.execute(f"CREATE DATABASE {sql_database}")
    print(f"Database {sql_database}, created successfully!")
except mysql.connector.Error as err:
    print(f"Database {sql_database} exists. We continue.")

sql_connect.close()
sql_cursor.close()

### Create Table

sql_connect= connect_to_mysql(sql_host,sql_user,sql_password,sql_database)
sql_cursor= sql_connect.cursor()

try:
    sql_cursor.execute("CREATE TABLE finance (id INT AUTO_INCREMENT PRIMARY KEY, value VARCHAR(255), date DATE, kind BOOLEAN)")
    print("Database finance, created succesfully!")
except mysql.connector.Error as err:
    print(f"The table exist, we continue.")

# Ask user for Expense or Revenue

def get_valid_input():
    while True:
        user_input = input("For Revenue press 0 and for expense press 1. Enter 0 or 1: ")
        if user_input in ['0', '1']:
            return int(user_input)
        else:
            print("Invalid input. Please enter either 0 or 1.")

while True:

    user_choice = get_valid_input()

# Insert Date

    date_input_str = input("Enter a date (YYYY-MM-DD): ")

# Convert the string to a datetime object
    try:
        date_input = datetime.strptime(date_input_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use the format YYYY-MM-DD.")


# Insert Decimal number

    user_input = input("Please enter a decimal number: ")

    try:
        decimal_number=float(user_input)
        print(f"You entered: {decimal_number}")
    except ValueError:
    # Handle the case where the user didn't enter a valid decimal number
        print("Invalid input. Please enter a valid decimal number.")




    sql = "INSERT INTO finance (value, kind, date) VALUES (%s, %s, %s)"
    val = (decimal_number, user_choice, date_input_str)

    sql_cursor.execute(sql,val)

    sql_connect.commit()

    exit_command = input("Enter 'exit' to stop or any other key to continue: ")
    if exit_command.lower() == 'exit':
        break  # Exit the main loop if the user inputs 'exit'



