# file for functions involving the Library Members table

from tabulate import tabulate


# Displays Library Members table
def table_members(cursor):
    cursor.execute("""SELECT memberID, member_name, address, phone_number, membership_date
                FROM LibraryMembers""")
    rows = cursor.fetchall()
    headers = ['MemberID', 'Name', 'Address', 'Phone Number', 'Join Date']
    print(tabulate(rows, headers=headers, tablefmt='grid'))

# Function to search in Library Members table
def member_custom_search(cursor):
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