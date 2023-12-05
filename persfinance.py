#!/usr/bin/env python3

import json,os

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
        sql_localhost= read_data["localhost"]
        sql_user= read_data["user"]
        sql_password= read_data["password"]
        sql_database= read_data["database"]
        print(f"You are going to connect to {sql_user}@{sql_localhost} and your password is {sql_password}\nand the database name is {sql_database}")

        
else:
    usr_input1= input('Enter the host(localhost): ')
    usr_input2= input('Enter the user of mysql: ')
    usr_input3= input('Enter the password of user: ')
    usr_input4= input('Enter the database name you want to create: ')

    with open('variables.json', 'w') as json_file:
        data = {
            "localhost": usr_input1,
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
        sql_localhost= read_data["localhost"]
        sql_user= read_data["user"]
        sql_password= read_data["password"]
        sql_database= read_data["database"]
        print(f"You are going to connect to {sql_user}@{sql_localhost} and your password is {sql_password}\nand the database name is {sql_database}")

