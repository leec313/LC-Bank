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



def login():
    """
    Prompts user to enter their name & password
    If name and password match, the user can access the next page
    And the next function will run
    Also acts as a logout function as when it is called, it will 
    return the user to the login screen
    """

def options():
    """
    Asks user to select options on what they would like to do next
    Options may include withdraw, deposit, check balance etc.
    """

def withdraw():
    """
    Allows user to withdraw from the account of their choosing
    Minus input amount from the current balance
    """

def deposit():
    """
    Allows user to deposit from the account of their choosing
    Adds input amount from the current balance
    """

def check():
    """
    Allows user to check the balance in the account of their choosing
    """

def main():
    """
    Initialises all program functions
    """

main()