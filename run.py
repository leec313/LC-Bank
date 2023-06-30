"""
LC Bank is a bank account system that allows a user to login,
create an account, check their balance, deposit, withdraw.
"""
import os
import gspread
from google.oauth2.service_account import Credentials

# Connecting Google Sheet to project
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('lc_bank')


def welcome():
    """
    Shows welcome message to user and moves on to the login function
    """
    building = """
                                                     ___
                                             ___..--'  .`.
                                    ___...--'     -  .` `.`.
                           ___...--' _      -  _   .` -   `.`.
                  ___...--'  -       _   -       .`  `. - _ `.`.
           __..--'_______________ -         _  .`  _   `.   - `.`.
        .`    _ /\    -        .`      _     .`__________`. _  -`.`.
         -   _ /  \_     -   .`  _         .` | WELCOME TO|`.   - `.`.
      .` -   _ /  \_     -   .`  _         .` |  LC BANK  |`.   - `.`.
    .`-    _  /   /\   -   .`        _   .`   |___________|  `. _   `.`.
  .`________ /__ /_ \____.`____________.`     ___       ___  - `._____`|
    |   -  __  -|    | - |  ____  |   | | _  |   |  _  |   |  _ |
    | _   |  |  | -  |   | |.--.| |___| |    |___|     |___|    |
    |     |--|  |    | _ | |'--'| |---| |   _|---|     |---|_   |
    |   - |__| _|  - |   | |.--.| |   | |    |   |_  _ |   |    |
 ---``--._      |    |   |=|'--'|=|___|=|====|___|=====|___|====|
 -- . ''  ``--._| _  |  -|_|.--.|_______|_______________________|
`--._           '--- |_  |:|'--'|:::::::|:::::::::::::::::::::::|
_____`--._ ''      . '---'``--._|:::::::|:::::::::::::::::::::::|
----------`--._          ''      ``--.._|:::::::::::::::::::::::|
`--._ _________`--._'        --     .   ''-----.................'
    """
    print(building)


def create_or_login():
    """
    Allows the user to choose login or create an account.
    Runs correct function depending on the input
    """
    while True:
        try:
            option = int(
                input("Press 1 to Login or 2 to create an account: \n"))
            if option == 1:
                login()
            elif option == 2:
                create_account()
        except ValueError:
            print("Invalid entry, please enter a valid option")
        else:
            break


def create_account():
    """
    Allows user to create an account, with details taken such as
    name and password. Then generates an ID number for login
    """

    # Get the data list from the "password" worksheet
    data = SHEET.worksheet("password").get_all_values()
    # Get the data list from the "current" worksheet
    current_data = SHEET.worksheet("current").get_all_values()

    print("Thanks for choosing to bank with us! Provide us with your details:")
    name = input("Name: \n")
    password = input("Password: \n")

    # Check if the name already exists in the data list
    existing_names = [row[0] for row in data[1:]]  # Exclude header row
    if name in existing_names:
        exists = """
        An account with that name already exists.
        You'll be taken back to previous screen
        """
        print(exists)
        create_or_login()

    # Generate ID based on the length of the data list
    new_id = str(len(data))

    # Append the new user data to the data list
    new_row = [name, password, new_id]
    data.append(new_row)

    # Update the "password" worksheet with the updated data
    SHEET.worksheet("password").update("A1:C", data)

    # Append the new account information to the "current" worksheet
    current_row = [name, "0", new_id]
    current_data.append(current_row)

    # Update the "current" worksheet with the updated data
    SHEET.worksheet("current").update("A1:C", current_data)

    print(f"Account created successfully! Your ID is {new_id}.")

    login()


def login():
    """
    Prompts user to enter their name & password
    If name and password match, the user can access the next page
    And the next function will run
    Also acts as a logout function as when it is called,
    it will Also acts as a logout function as when it is called
    """
    # Getting the user and password data from the worksheet
    user_data = SHEET.worksheet("password").get_all_values()

    names = []
    passwords = []
    ids = []

    # taking the user data and assigning it to corresponding elements
    for sublist in user_data[1:]:  # Start from index 1 to skip the header row
        names.append(sublist[0])
        passwords.append(sublist[1])
        ids.append(sublist[2])

    while True:
        print("\nForgot your ID? Press 'F'\n")
        input_1 = input("Enter your ID:\n")

        if input_1 == "f":
            forgot_id()
            break
        else:
            print("\nForgot your password? Press 'P'\n")
            input_2 = input("Enter your password:\n")
            if input_2 == "p":
                forgot_password()
                break
            else:
                for i, (user_id, password) in enumerate(zip(ids, passwords)):
                    if input_1 == user_id and input_2 == password:
                        name = names[i]
                        clear_term()
                        print(
                            f"Welcome to LC Bank, {name}!\n")
                        options(user_id)
                        break
                else:
                    print("Invalid ID or password. Please try again.")
                    continue
                break


def options(user_id):
    """
    Asks user to select options on what they would like to do next
    Options may include withdraw, deposit, check balance etc.
    """
    print(f"ID: {user_id}\n")
    while True:
        try:
            print("1: Deposit")
            print("2: Withdraw")
            print("3: Check Balance")
            print("4: Logout")
            selection = int(
                input("Select one of the options above to get started:\n"))

            if selection == 1:
                transaction(user_id, "deposit")
                break
            if selection == 2:
                transaction(user_id, "withdraw")
                break
            if selection == 3:
                transaction(user_id, "check")
                break
            if selection == 4:
                main()
            else:
                clear_term()
                print(
                    "Invalid! Enter a valid option.\n")
                continue
            break
        except ValueError:
            print(
                "Invalid! Enter a valid option.\n")


def transaction(user_id, transaction_type):
    """
    Performs the deposit, withdrawal,
    or balance check transaction for the user.
    """

    worksheet = SHEET.get_worksheet(0)
    data = worksheet.get_all_values()[1:]  # Skip the header row

    # Find the user ID and retrieve the corresponding balance value
    balance = None
    user_row = None
    for row in data:
        if row[2] == user_id:
            user_row = row
            balance = float(row[1])
            break

    # Error handling so if there is no user ID somehow
    if balance is None:
        print("User ID not found.")
        return

    if transaction_type == "deposit":
        amount = float(input("Enter deposit amount: "))
        balance += amount
        print(f"Deposited {amount} successfully.")
        back(user_id)
    elif transaction_type == "withdraw":
        amount = float(input("Enter withdrawal amount: "))
        if balance < amount:
            print("Insufficient balance.")
            return
        balance -= amount
        print(f"Withdrawn {amount} successfully.")
        back(user_id)
    elif transaction_type == "check":
        print(f"Your balance is: {balance}")
        return
        back(user_id)

    # Update the balance value in the worksheet
    user_row[1] = str(balance)
    # Get the cell address for the user's balance
    cell_address = f"B{data.index(user_row) + 2}"
    worksheet.update(cell_address, str(balance))


def clear_term():
    """
    Clears the terminal to give the user a better, clearer view
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def back(user_id):
    """
    Gives the user the option to either go back to the
    login screen or the Menu
    """

    while True:
        try:
            next_option = input(
                "Press 1 to be taken back to the Menu or 2 to logout:\n")
            if next_option == "1":
                clear_term()
                options(user_id)
            elif next_option == "2":
                clear_term()
                main()
            else:
                clear_term()
                print("Enter a valid option")
        except ValueError:
            print("Enter a valid option")


def forgot_id():
    """
    Allows user to type in their name and it gives them their ID
    """
    clear_term()
    # Getting the user and password data from the worksheet
    user_data = SHEET.worksheet("password").get_all_values()

    names = []
    user_ids = []

    # taking the user data and assigning it to corresponding elements
    for sublist in user_data[1:]:  # Start from index 1 to skip the header row
        names.append(sublist[0])
        user_ids.append(sublist[2])

    user_input = input("Enter your name: \n")

    # Checking the input data against the spreadsheet data
    for i, (name, user_id) in enumerate(zip(names, user_ids)):
        if user_input == name:  # Compare the user input with the name
            user_id = user_ids[i]  # Get the corresponding user ID
            clear_term()
            print(f"{user_input}, your ID is: {user_id}.\n")
            break

    login()


def forgot_password():
    """
    Allows user to type in their ID and it gives them their password
    """
    clear_term()
    # Getting the user and password data from the worksheet
    user_data = SHEET.worksheet("password").get_all_values()

    passwords = []
    user_ids = []

    # taking the user data and assigning it to corresponding elements
    for sublist in user_data[1:]:  # Start from index 1 to skip the header row
        passwords.append(sublist[1])
        user_ids.append(sublist[2])

    user_input = input("Enter your ID: \n")

    # Checking the input data against the spreadsheet data
    for i, (password, user_id) in enumerate(zip(passwords, user_ids)):
        if user_input == user_id:  # Compare the user input with the name
            password = passwords[i]  # Get the corresponding user ID
            clear_term()
            print(f"Your password is: {password}.\n")
            break

    login()


def main():
    """
    Initialises all program functions
    """
    welcome()
    create_or_login()


main()
