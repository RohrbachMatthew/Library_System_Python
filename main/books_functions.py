# file for functions involving the Books table

from tabulate import tabulate

#  Displays Books table
def table_books(cursor):
    cursor.execute("""SELECT bookID, title, author, category, ISBN, publication_date, available_copies
                From Books""")
    rows = cursor.fetchall()
    headers = ['BookID', 'Title', 'Author', 'Category', 'ISBN', 'Date Published', 'Copies']
    print(tabulate(rows, headers=headers, tablefmt='grid'))

#  View books table by custom search
def book_search(cursor):
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
