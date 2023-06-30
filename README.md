![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

Welcome,

This is the Code Institute student template for deploying your third portfolio project, the Python command-line project. The last update to this file was: **March 14, 2023**

## Reminders

- Your code must be placed in the `run.py` file
- Your dependencies must be placed in the `requirements.txt` file
- Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

---

Happy coding!


def deposit(user_id):
    """
    Allows user to deposit from the account of their choosing
    Adds input amount from the current balance
    """
    current_sheet = SHEET.worksheet("current")
    current_data = current_sheet.get_all_values()

    # Getting the current account balance and taking it in a float
    for row in current_data[1:]:
        if row[2] == user_id:
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
    back(user_id)


def withdraw(user_id):
    """
    Allows user to withdraw from the account of their choosing
    Minus input amount from the current balance
    """
    current_sheet = SHEET.worksheet("current")
    current_data = current_sheet.get_all_values()

    # Getting the current account balance and taking it in a float
    for row in current_data[1:]:
        if row[2] == user_id:
            current_balance = float(row[1])
            # Adding 1 to account for header row
            row_index = current_data.index(row) + 1
            break

    # Taking the user's input for the withdrawal amount as a float
    while True:
        withdraw_amount = float(
            input("Please enter the amount you wish to withdraw: $\n"))

        # Check if the user's current balance is less than withdrawal input
        if withdraw_amount > current_balance:
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
    back(user_id)


def check(user_id):
    """
    Allows user to check the balance in the account of their choosing
    """
    current_sheet = SHEET.worksheet("current")
    current_data = current_sheet.get_all_values()

    # Getting the current account balance and taking it in a float
    for row in current_data[1:]:
        if row[2] == user_id:
            current_balance = float(row[1])
            break
    print(f"\nYour current account balance is {current_balance}.\n")
    back(user_id)
