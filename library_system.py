"""
Program uses MySQL database: Library to make SQL queries
    - Displays Main Menu with options
    - User selects option and follows prompts for queries
    - Table / Row / Data shows with small menu under to go back to main or quit

TODO: add user login for security default:
                                  UserName: Admin1
                                  Password: PassWord!123
    - add error handling
    - add comments and doc
    -
    - make errors for add loans function (no date entered, invalid print for each input)
    -
    - make a book loans return function
"""

# imports functions from file names
from members_functions import table_members, member_custom_search
from books_functions import table_books, book_search
from bookLoans_functions import table_loans, add_loans

import mysql.connector


# Connection to MySQL database
"""
Connection replaced with ***** for security
    -Download the csv files located in library repository
    -Create host,user,password and database name for the database then replace
"""
connection = mysql.connector.connect(
    host="***********",
    user="********",
    password="********",
    database="**********"
)

#  Cursor connects to interact with database
cursor = connection.cursor()


#  Main menu for program
def main_menu():
    print("Main Menu:\n1. View Books Table\n2. View LibraryMembers Tabel\n3. View BookLoans Table\n"
          "4. Custom Search For Member In LibraryMembers Table.\n5. Start New Book Loan.\n"
          "6. Search for a Book ")


while True:
    main_menu()
    user = input("Enter choice: ")
    #  Quit program
    if user.lower() == 'quit':
        break
    #  Option 1
    elif user == '1':
        print("Books Table:")
        table_books(cursor)
        if input("Menu:\n1. Back to main menu\n2. Quit program\nEnter choice: ") == '1':
            print()  # Leaves space between menus
            continue
        else:
            break
    #  Option 2
    elif user == '2':
        print("Members Table:")
        table_members(cursor)
        if input("Menu:\n1. Back to main menu\n2. Quit program\nEnter choice: ") == '1':
            print()  # Leaves space between menus
            continue
        else:
            break
    #  Option 3
    elif user == '3':
        print("Book Loans Table:")
        table_loans(cursor)
        if input("Menu:\n1. Back to main menu\n2. Quit program\nEnter choice: ") == '1':
            print()  # Leaves space between menus
            continue
        else:
            break
    #  Option 4
    elif user == '4':
        member_custom_search(cursor)
        if input("Menu:\n1. Back to main menu\n2. Quit program\nEnter choice: ") == '1':
            print()  # Leaves space between menus
            continue
        else:
            break
    #  Option 5
    elif user == '5':
        add_loans(cursor, connection)
        while True:
            user_choice = input("Menu:\n1. Back to main menu\n2."
                                " perform another loan\nEnter Choice:")
            if user_choice == '2':
                add_loans(cursor, connection)
            elif user_choice == '1':
                break
            else:
                print("INVALID")

    # Option 6
    elif user == '6':
        book_search(cursor)
        while True:  # Loop for searching again
            user_choice = input("Menu:\n1. Perform another search\n"
                                "2. Main menu\nEnter Choice:")
            if user_choice == '1':
                book_search(cursor)
            elif user_choice == '2':  # If 2 exits loop
                break
            else:  # Invalid Choice
                print("INVALID")

    # Invalid choice for main loop
    else:
        print("Invalid Choice")

# Close out the cursor and connection
cursor.close()
connection.close()
print("Exiting Program")
