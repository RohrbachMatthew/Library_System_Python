"""
Program uses MySQL database: Library to make SQL queries
    - Displays Main Menu with options
    - User selects option and follows prompts for queries
    - Table / Row / Data shows with small menu under to go back to main or quit

TODO: add take away from available copies function for loans
TODO: add error handling
TODO: add comments and doc
"""
from datetime import date
import mysql.connector
from tabulate import tabulate

"""
Connection replaced with ***** for security
    -Download the csv files located in library repository
    -Create host,user,password and database name for the database then replace
"""
connection = mysql.connector.connect(
    host='*********',  #  Enter host name
    user='*********',  #  Enter username
    password='********',  #  Enter password
    databse='********'  #  Enter database name
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
    Prompts user for parameters, performs a custom search query in LibraryMembers table
    - column_select: column/columns to be displayed in query result
    - column_filter: column to be used for WHERE filter
    - user_value: The value to be searched inside the column_filter
    - placeholder %s in query protects from injections
    """
    column_select = input("Enter columns to display seperated by a comma : ")
    column_filter = input("Enter column to find member with: ")
    user_value = input("Enter value of column: ")

    #  Query for database
    query = f"SELECT {column_select} FROM LibraryMembers WHERE {column_filter} = %s"
    #  Executes query with parameter user_value
    cursor.execute(query, (user_value,))
    #  Fetch one row that matches the query values
    table = cursor.fetchone()
    print(table)

#  Add to BookLoans table
def add_loans():
    """
    - date.today get the current date
    """
    user_loan_id = input("Enter new loan ID: ")
    user_book_id = input("Enter book ID")
    user_member_id = input("Enter member ID")
    get_date = date.today()  # Get current date
    today_date = f"{get_date:%Y-%m-%d}"  # F string to format yyy-mm-dd
    date_due = input("Enter Due Date (YYYY-MM-DD): ")
    query = (f"INSERT INTO BookLoans (loanID, bookID, memberID, date_borrowed, due_date, date_returned)"
             f"VALUES (%s, %s, %s, %s, %s, %s)")
    values = [user_loan_id, user_book_id, user_member_id, today_date, date_due, None]  # None for Null in MySQL
    cursor.execute(query, values)
    connection.commit()  # commits to database
    print(f"Added LoanID: {user_loan_id}, BookID: {user_book_id}, MemberID: {user_member_id},"
          f" Due Date: {date_due} successfully!")


#  Main menu for program
def main_menu():
    print("Main Menu:\n1. View Books Table\n2. View LibraryMembers Tabel\n3. View BookLoans Table\n"
            "4. Custom Search For Member In LibraryMembers Table.\n5. Start New Book Loan.")

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
        if input("Menu:\n1. Back to main menu\n2. Quit program\nEnter choice: ") == '1':
            print()  # Leaves space between menus
            continue
        else:
            break
    else:
        print("Invalid Choice")
cursor.close()
connection.close()
print("Exiting Program")
