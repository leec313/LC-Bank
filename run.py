import os
import gspread
from google.oauth2.service_account import Credentials

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
                print(option)
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
        input_1 = input("Enter your ID:\n")
        input_2 = input("Enter your password:\n")

        for i, (id, password) in enumerate(zip(ids, passwords)):
            if input_1 == id and input_2 == password:
                name = names[i]
                clear_term()
                print(f"Welcome {name}! Thanks for banking with LC Bank.\n")
                options(id)
                break
        else:
            print("Invalid ID or password. Please try again.")
            continue
        break


def options(id):
    """
    Asks user to select options on what they would like to do next
    Options may include withdraw, deposit, check balance etc.
    """
    print(f"ID: {id}\n")
    while True:
        print("1: Deposit")
        print("2: Withdraw")
        print("3: Check Balance")
        print("4: Logout")
        print("5: Exit")
        selection = int(
            input("Please select one of the options above to get started:\n"))

        if selection == 1:
            deposit(id)
            break
        elif selection == 2:
            withdraw(id)
            break
        elif selection == 3:
            check(id)
            break
        elif selection == 4:
            main()
        elif selection == 5:
            exit()
        else:
            print(
                f"Invalid! You entered {selection}, enter a valid option:\n")
            continue
        break


def deposit(id):
    """
    Allows user to deposit from the account of their choosing
    Adds input amount from the current balance
    """
    current_sheet = SHEET.worksheet("current")
    current_data = current_sheet.get_all_values()

    # Getting the current account balance and taking it in a float
    for row in current_data[1:]:
        if row[2] == id:
            current_balance = float(row[1])
            # Adding 1 to account for header row
            row_index = current_data.index(row) + 1
            break

    # Taking the user's input for the deposit amount as a float
    deposit_amount = float(
        input("Please enter the amount you wish to deposit: $\n"))

    # Clearing terminal for better viewing
    clear_term()

    # Calculation for new balance
    new_amount = current_balance + deposit_amount

    print(f"Success! You have deposited ${deposit_amount}!")
    print(f"Your new balance is ${new_amount}.\n")

    # Updating the balance in the worksheet
    current_sheet.update_cell(row_index, 2, new_amount)

    # Gives option to user on what to do next
    back(id)


def withdraw(id):
    """
    Allows user to withdraw from the account of their choosing
    Minus input amount from the current balance
    """
    current_sheet = SHEET.worksheet("current")
    current_data = current_sheet.get_all_values()

    # Getting the current account balance and taking it in a float
    for row in current_data[1:]:
        if row[2] == id:
            current_balance = float(row[1])
            # Adding 1 to account for header row
            row_index = current_data.index(row) + 1
            break

    # Taking the user's input for the withdrawal amount as a float
    while True:
        withdraw_amount = float(
            input("Please enter the amount you wish to withdraw: $\n"))

        # Check if the user's current balance is less than withdrawal input
        if (withdraw_amount > current_balance):
            print("You have insufficient funds!")
            continue

        elif withdraw_amount < current_balance:
            # Clearing terminal for better viewing
            clear_term()
            # Calculation for new balance
            new_amount = current_balance - withdraw_amount

            print(f"Success! You have withdrawn ${withdraw_amount}!")
            print(f"Your new balance is ${new_amount}.\n")

            # Updating the balance in the worksheet
            current_sheet.update_cell(row_index, 2, new_amount)
            break

    # Gives option to user on what to do next
    back(id)


def check(id):
    """
    Allows user to check the balance in the account of their choosing
    """
    current_sheet = SHEET.worksheet("current")
    current_data = current_sheet.get_all_values()

    # Getting the current account balance and taking it in a float
    for row in current_data[1:]:
        if row[2] == id:
            current_balance = float(row[1])
            break
    print(f"\nYour current account balance is {current_balance}.\n")
    back(id)


def clear_term():
    """
    Clears the terminal to give the user a better, clearer view
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def back(id):
    """
    Gives the user the option to either go back to the 
    login screen or the Menu
    """

    while True:
        try:
            next_option = input(
                "Press 1 to be taken back to the Menu or 2 to logout:\n")
            if next_option == "1":
                options(id)
            elif next_option == "2":
                main()
            else:
                clear_term()
                print("Enter a valid option")
        except ValueError:
            print("Enter a valid option")


def main():
    """
    Initialises all program functions
    """
    welcome()
    create_or_login()


main()
