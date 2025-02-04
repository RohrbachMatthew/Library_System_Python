#  Install packages if needed (mysql.connector, tabulate)
import mysql.connector
from tabulate import tabulate

#  Connection for mysql database (replace placeholders with your information)
connection = mysql.connector.connect(
    host='*********',  #  Enter host name
    user='*********',  #  Enter username
    password='********',  #  Enter password
    databse='********'  #  Enter database name
)

cursor = connection.cursor()  #  Connects and sets cursor as cursor

#  MySQL commands for query ordered by categories
cursor.execute("""SELECT bookID, title, author, category, ISBN, publication_date, available_copies
            From Books
            ORDER BY category""")

rows = cursor.fetchall()  #  gets all from the rows in the query

#  makes headers for the rows from query
headers = ['BookID', 'Title', 'Author', 'Category', 'ISBN', 'Date Published', 'Copies']

#  Prints out table in grid format
print(tabulate(rows, headers=headers, tablefmt="grid"))

#  Closes out the cursor and the connection when done
cursor.close()
connection.close()