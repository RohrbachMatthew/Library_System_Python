# file for functions involving the Book Loans table

from tabulate import tabulate
from datetime import date

#  Displays BookLoans table
def table_loans(cursor):
    cursor.execute(f"SELECT loanID, bookID, memberID, date_borrowed, due_date, date_returned "
                   f"FROM BookLoans")
    rows = cursor.fetchall()
    headers = ['loanID', 'bookID', 'memberID', 'date_borrowed', 'due_date', 'date_returned']
    print(tabulate(rows, headers=headers, tablefmt='grid'))


#  Add to BookLoans table
def add_loans(cursor, connection):  # cursor object used to read database, connection is used to modify
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
        Inserts into BookLoans and Updates Books if available_copies is more than 0
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