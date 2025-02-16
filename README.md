# Python Library Management System
## Overview
Python file that interacts with the MySQL Library database
- Main System File:
   - [library_system.py](https://github.com/RohrbachMatthew/Library_System_Python/blob/master/library_system.py)
- Function Files located in .venv folder:
  - [bookLoans_functions.py](https://github.com/RohrbachMatthew/Library_System_Python/blob/master/.venv/bookLoans_functions.py)
  - [books_functions.py](https://github.com/RohrbachMatthew/Library_System_Python/blob/master/.venv/books_functions.py)
  - [members_functions.py](https://github.com/RohrbachMatthew/Library_System_Python/blob/master/.venv/members_functions.py)
## Functions
1. View all rows in each table
2. Search Books by specific column and value
3. Search Members by column and value
4. Add Loans
    - checks available copies in Books
    - adds loan and deletes one copy from books by bookID
5. Main Loop

## Database

- Goto [my_library MySQL](https://github.com/RohrbachMatthew/Library)
for the MySQL database set up, query files, and original data.