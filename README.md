# LC Bank
## A Python Command Line Bank Account System

This application is a Python based bank account system. It allows the user to login or create an account. Once the user has an account, they can deposit, withdraw, check their balance and use the forget ID/Password feature. All of the information is linked to a [Google Sheet which can be found here.](https://docs.google.com/spreadsheets/d/1Q7y4NdUdrZLA8RSyJG3h7YuQ12M_Dei93Oz3sv0oGXU/edit?usp=sharing) The data writes and reads to the sheet where the information can be accessed by the user once they login. 

### - By Lee Curtis

### [Live site](https://lc-bank-4b2b0ce68329.herokuapp.com/)

## Table of contents

 1. [ Pre-Project Planning ](#plan)  
 2. [ Features Left to Implement ](#left)  
 3. [ Technology used ](#tech) 
 4. [ Testing ](#testing)  
 5. [ Bugs ](#bugs)  
 6. [ Deployment](#deployment)
 7. [ Credits](#credits)
 8. [ Content](#content)  
 9. [ Acknowledgements](#acknowledgements)  


## Flow

<a name="plan"></a>

## Pre-project Planning

I chose to develop a banking system using Python as my project 3. After finalizing this idea, I began mapping out the workflow and utilized Lucid Chart to generate a user-friendly process diagram. I created this diagram early on to grasp the necessary logic for project completion and determine the sequential steps for implementation. To gain a clearer understanding of the initial design and concept, please refer to the provided flow chart below. The initial design may have changed slightly as I implemented features such as the forgot password/ID function, however the base concept is relatively the same. 

Flow chart here

## User Stories

- With the bank account program, I can securely access my account whenever needed.
- The bank account program should provide a seamless account creation process.
- I should be able to conveniently check my account balance using the program.
- The program should allow me to effortlessly deposit funds into my account.
- With the program, I can easily withdraw money from my account whenever required.
- In case I forget my password or ID, the program should provide an easy way to recover them.
- I should be able to securely log out of my bank account using the program.

## Pre-Planning Structure

### Structure

### Google Sheet Structure

### 2 worksheets 
- 1st worksheet ("current" - Current Account): 
    - Name
    - Amount
    - ID
- 2nd worksheet ("password" - For passwords):
    - Name
    - Password
    -ID

By organizing the Google Sheets file in the aforementioned manner, I obtained a clear vision of how I intended to access the user data. Looking back, I could have opted for a single worksheet, but for the sake of my own understanding, I determined it was more advantageous to proceed in this manner.

### Program Structure

Initially, the program consisted of multiple functions, but through the process of code refactoring, I was able to enhance its efficiency. Specifically, I combined the deposit, withdraw, and check balance functions into a single function, realizing a more streamlined code structure. Additionally, the forget password and forget ID functions were merged, as they shared similar code blocks. Below is the initial code snippet that implemented these features.

### Initial setup for Deposit, Withdraw and Check Balance
```
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
```

_______________________________________________________________________________________________________

### Initial setup for Forgot password and forgot ID 

```
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
```

Following the code refactoring process, the final implementation comprised a total of 10 functions. Among these functions, there were additional smaller functions incorporated to enhance the user experience. For instance, an accessible feature to clear the terminal was included to provide a more convenient viewing experience for the user. Additionally, a back function was implemented, offering the user the flexibility to either log out or return to the options screen or main menu upon completing an action.

### Program Flow

- When the program starts, the user is presented with the welcome message that is ASCII art of the bank building
- They are presented with options to either login or create an account:
LOGIN OR CREATE ACCOUNT IMAGE
- If the user selects login, they can enter their ID and Password. 
LOGIN DETAILS IMAGE
- They also have the option to select "f" or "F" if they have forgotten their ID and "p" or "P" if they have
forgotten their password. If they select either of these options, they will be asked for their Name and it will
show them their ID or they will input their ID if they forgot their password. 
FORGOT IMAGES HERE
- Once logged in, they are shown the main menu or options:
OPTIONS IMAGE
- If they select 1, they will be asked how much they would like to deposit. If they enter an invalid value, they will be taken back to 
the main menu. If they enter a valid amount, it will be added to their account and the Google Sheet will be updated.
DEPOSIT IMAGE
- If they select 2, they will be asked how much they would like to withdraw. If they enter an invalid value, they will be taken back to 
the main menu. If they enter a valid amount, it will be subtracted from their account and the Google Sheet will be updated.
WITHDRAW IMAGE
- If the user selects 3, the program will display the current balance of their account from the data taken from the Google Sheet. 
CHECK IMAGE
- After each action/option is completed, they will be asked if they would like to go back to the main menu or logout. 
BACK IMAGE
- The final option in the main menu list is 4 and that is logout. This takes them back to the welcome message and asks if they would
like to login or create an account. 
- If the user decides to create an account, the program will ask them for their name and tell them to choose a password:
CREATE ACCOUNT IMAGES
- From there, an ID is generated based on the next available value from the Google Sheet. So for example, if the last account ID added to the sheet is
20, the next user who creates an account will have the ID of 21:
ID IMAGE
- Once the account is created, they are taken to the login screen.

<a name="left"></a>

## Features left to implement

- Two Factor Authentication: 
    To enhance the login process and the functionality of the "forgot credentials" feature, it would be beneficial to implement a system that sends a text message to the user containing a randomly generated 6-digit code. The user would need to enter the correct code to proceed, and if incorrect, they would be prompted to try again. This implementation would require linking the user's phone number to their account within the Google Sheet, as well as incorporating more advanced coding techniques into the program.

- More use of ASCII art
    In order to enhance the user experience, it could have been advantageous to incorporate additional ASCII art into the program. Alternatively, I chose to utilize Colorama, which enables the modification of text and background colors. Although the combined use of both ASCII art and Colorama could have potentially elevated the overall experience further.

- More options in the main menu
  Including additional options in the main menu, such as the ability to choose other account types like Credit, Savings, and so on, could have been beneficial. However, due to time constraints and feasibility considerations, I decided to stick with a single account type, namely "current." If I had more time available, I believe implementing these additional options would have been relatively straightforward.

- Transaction History
    Implement a feature that allows users to view their transaction history, providing them with a detailed record of their deposits, withdrawals, and account balance changes.

- Account Statements
    Provide users with the ability to generate and download account statements in a printable format, summarizing their financial activities within a specific time period.

- Interest Calculation
    Introduce an interest calculation feature that calculates and updates the account balance based on a predefined interest rate and compounding frequency.


<a name="tech"></a>

# Technology Used
### [Python](https://en.wikipedia.org/wiki/Python_(programming_language))
Used to create the application

### [Heroku](https://heroku.com)
Used to deploy and host the application

### [Github](https://github.com)
Used to store the code

### [Gitpod](https://gitpod.io)
IDE used for creating the application

### [Git](https://en.wikipedia.org/wiki/Git)
Used for version control

### [Colorama](https://pypi.org/project/colorama/)
Used for injecting color into various ares for increased clarity

### [Google Sheets/Drive API](https://developers.google.com/sheets/api/reference/rest)
Used for storing and accessing user data


<a name="testing"></a>

# Testing

## Testing Phase

### Manual Testing

| Test | Result |
|--|--|
|On run program, the welcome message appears|Pass|
|After welcome message user prompted to login or create an account|Pass|
|When option is selected, correct function runs|Pass|
|Select 1, login screen appears|Pass|
|Selecting 2 prompted to create an account and data is updated in the Google Sheet|Pass|
|At login, user can choose forget password/ID option and they work as intended|Pass|
|After login, main menu of options appear and shows the ID of the user|Pass|
|All options work as intended and updated/access the data sheet as necessary|Pass|
|Logout option brings the user back to the welcome screen and forgets the user ID|Pass|

### User tests

The following tests are on the error handling throughout the project. If the error handling works as expected it will be marked as pass. If it does not work as expected then it will be marked as a fail.

    Create or Login test - on startup, the user can select only 2 options. Press 1 or press 2 - anything else will provide an error and ask them to try again.
| Test | Result |
|--|--|
|Program start, user enters anything other than 1 or 2 throws error|Pass|
|Press 1, allows user to login|Pass|
|Press 2, allows user to create an account|Pass|
|At login, the user should enter their ID, then their password. If either do not match, they are shown an error message and will be asked to try again.|Pass|

    At login, if the user forgets their ID or password, they can press F or P respectively to gain access to this data. 
|If there is no matching name for the corresponding ID, they will be shown an error and asked to try again|Pass|
||Pass|

