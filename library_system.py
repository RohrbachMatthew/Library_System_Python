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
    - start to separate functions into different files for organization
"""

from datetime import date
import mysql.connector
from tabulate import tabulate

# Connection to MySQL database
"""
Connection replaced with ***** for security
    -Download the csv files located in library repository
    -Create host,user,password and database name for the database then replace
"""
connection = mysql.connector.connect(
    host="*********",
    user="********",
    password="*******",
    database="********"
)

#  Cursor connects to interact with database
cursor = connection.cursor()


#  Displays Books table
def table_books():
    cursor.execute("""SELECT bookID, title, author, category, ISBN, publication_date, available_copies
                From Books""")
    rows = cursor.fetchall()
    headers = ['BookID', 'Title', 'Author', 'Category', 'ISBN', 'Date Published', 'Copies']
    print(tabulate(rows, headers=headers, tablefmt='grid'))


#  Displays LibraryMembers table
def table_members():
    cursor.execute("""SELECT memberID, member_name, address, phone_number, membership_date
                FROM LibraryMembers""")
    rows = cursor.fetchall()
    headers = ['MemberID', 'Name', 'Address', 'Phone Number', 'Join Date']
    print(tabulate(rows, headers=headers, tablefmt='grid'))


#  Displays BookLoans table
def table_loans():
    cursor.execute(f"SELECT loanID, bookID, memberID, date_borrowed, due_date, date_returned "
                   f"FROM BookLoans")
    rows = cursor.fetchall()
    headers = ['loanID', 'bookID', 'memberID', 'date_borrowed', 'due_date', 'date_returned']
    print(tabulate(rows, headers=headers, tablefmt='grid'))


def member_custom_search():
    """
    Prompts user for parameters, performs a custom search query based on input (column
    name and value) to search in LibraryMembers table:
        - column_filter: column to be used for WHERE filter
        - user_value: The value to be searched inside the column_filter
        - placeholder %s in query protects from injections
    """
    column_filter = input("Enter column to find member with: ")
    user_value = input("Enter value: ")

    #  Query for database
    query = f"SELECT * FROM LibraryMembers WHERE {column_filter} IN %s"

    value = [user_value]
    #  Executes query with parameter value
    cursor.execute(query, value)
    #  Fetch rows that matches the query values
    rows = cursor.fetchall()
    headers = ['MemberID', 'Name', 'Address', 'Phone Number', 'Join Date']
    print(tabulate(rows, headers=headers, tablefmt='grid'))


#  View books table by custom
def book_search():
    """
    Prompts user for column and value to show specific book row:
        - user_column: column to be used for WHERE
        - user_search: The value to be searched inside the column_filter
        - placeholder %s in query protects from injections replaces with value
        - executes query and value from user
        - fetches all filtered rows
        - adds headers and prints out table
    """
    user_column = input("Enter column to search with: ")
    user_search = input("Enter value: ")
    search_query = (f"select * from Books "
                    f"Where {user_column} = %s")

    value = [user_search]  # value for placeholder

    cursor.execute(search_query, value)
    rows = cursor.fetchall()

    headers = ['BookID', 'Title', 'Author', 'Category', 'ISBN', 'Date Published', 'Copies']
    print(tabulate(rows, headers=headers, tablefmt='grid'))


#  Add to BookLoans table
def add_loans():
    """
    - get loanID, bookID, memberID, and due date from user
    - date.today get the current date
    - formats the current date to match database format YYY-MM-DD
    - get due date from user
    - checks available_copies in Books through query
    - executes as tuple (user_book_id,)
    - if copies are more than 0 adds the loan
    - if copies are 0 prints no copies available
    """
    user_loan_id = input("Enter new loan ID: ")
    user_book_id = input("Enter book ID")
    user_member_id = input("Enter member ID")

    get_date = date.today()  # Get current date
    today_date = f"{get_date:%Y-%m-%d}"  # F string to format yyy-mm-dd

    date_due = input("Enter Due Date (YYYY-MM-DD): ")

    # Check if there are available_copies
    check_copies = (f"Select available_copies from Books "
                    f"where bookID = %s")
    cursor.execute(check_copies, (user_book_id,))  # Gets the row, makes tuple
    copies = cursor.fetchone()[0]  # fetches at 0 index (available_copies)

    if copies > 0:
        """
        Inserts into BookLoans and Updates Books
        - query inserts into BookLoans using place holders
        - uses values from user input
        - executes the query with values inserted
        - updates the available copies in Books to take one away from available_copies
        - prints a message to notify the information was added
        """
        query = (f"INSERT INTO BookLoans (loanID, bookID, memberID, date_borrowed, due_date, date_returned)"
                 f"VALUES (%s, %s, %s, %s, %s, %s)")
        values = [user_loan_id, user_book_id, user_member_id, today_date, date_due, None]  # None for Null in MySQL
        cursor.execute(query, values)

        #  delete one copy from available copies in books table by book id loan
        update_copies = (f"UPDATE Books "
                         f"SET available_copies = available_copies - 1 "
                         f"WHERE bookID = %s")
        value = [user_book_id]
        cursor.execute(update_copies, value)

        connection.commit()  # commits to database
        print(f"Added LoanID: {user_loan_id}, BookID: {user_book_id}, MemberID: {user_member_id},"
              f" Due Date: {date_due} successfully!")
    else:  # If no copies available
        print("No Copies Available")


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
        table_books()
        if input("Menu:\n1. Back to main menu\n2. Quit program\nEnter choice: ") == '1':
            print()  # Leaves space between menus
            continue
        else:
            break
    #  Option 2
    elif user == '2':
        print("Members Table:")
        table_members()
        if input("Menu:\n1. Back to main menu\n2. Quit program\nEnter choice: ") == '1':
            print()  # Leaves space between menus
            continue
        else:
            break
    #  Option 3
    elif user == '3':
        print("Book Loans Table:")
        table_loans()
        if input("Menu:\n1. Back to main menu\n2. Quit program\nEnter choice: ") == '1':
            print()  # Leaves space between menus
            continue
        else:
            break
    #  Option 4
    elif user == '4':
        member_custom_search()
        if input("Menu:\n1. Back to main menu\n2. Quit program\nEnter choice: ") == '1':
            print()  # Leaves space between menus
            continue
        else:
            break
    #  Option 5
    elif user == '5':
        add_loans()
        while True:
            user_choice = input("Menu:\n1. Back to main menu\n2."
                                " perform another loan\nEnter Choice:")
            if user_choice == '2':
                add_loans()
            if user_choice == '1':
                break
            else:
                print("INVALID")

    # Option 6
    elif user == '6':
        book_search()
        while True:  # Loop for searching again
            user_choice = input("Menu:\n1. Perform another search\n"
                                "2. Main menu\nEnter Choice:")
            if user_choice == '1':
                book_search()
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
