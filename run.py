import gspread
from google.oauth2.service_account import Credentials
import os

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
        input_1 = input("Enter your ID: ")
        input_2 = input("Enter your password: ")

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
        input("Please enter the amount you wish to deposit: $"))

    # Clearing terminal for better viewing
    clear_term()

    # Calculation for new balance
    new_amount = current_balance + deposit_amount

    print(f"Success! You have deposited ${deposit_amount}!")
    print(f"Your new balance is ${new_amount}.")

    # Updating the balance in the worksheet
    current_sheet.update_cell(row_index, 2, new_amount)


def withdraw(id):
    """
    Allows user to withdraw from the account of their choosing
    Minus input amount from the current balance
    """


def check(id):
    """
    Allows user to check the balance in the account of their choosing
    """


def clear_term():
    """
    Clears the terminal to give the user a better, clearer view
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    """
    Initialises all program functions
    """
    welcome()
    login()


main()
