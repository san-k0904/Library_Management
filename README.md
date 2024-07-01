Library Management System
=========================

This project is a Library Management System developed to demonstrate and implement my learning of Python and MySQL. The system allows for the management of books and members, facilitating typical library operations such as adding, removing, and updating records.

Features
--------

-   **Database Setup**: Automatically creates and connects to a MySQL database named `LIBRARY_MANAGEMENT`.
-   **Book Management**: Allows adding, updating, and removing books. Stores details such as Book ID, Book Name, Author Name, Genre, Series Name, Series Number, and Quantity.
-   **Member Management**: Allows adding, updating, and removing members. Stores details such as Member Name, Member ID, Phone Number, Address, and Membership Type.
-   **Transaction Handling**: Manages the borrowing and returning of books by members, keeping track of issued books.

Installation
------------

To set up this Library Management System, follow these steps:

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/library-management-system.git
    
    cd library-management-system
    ```

3.  **Install dependencies**: Ensure you have `MySQLdb` installed. If not, you can install it using pip:

    ```bash
    pip install mysqlclient
    ```

5.  **Configure MySQL**:

    -   Start your MySQL server.
    -   Update the MySQL connection details in the `Library_mangement.py` script if necessary:

      ```  python
        db = MySQLdb.connect(host='localhost', user='root', password='yourpassword')
      ```

6.  **Run the script**:

    ```bash
    
    python Library_mangement.py
    ```

Usage
-----

-   The script will create the necessary database and tables if they do not already exist.
-   You can interact with the system through the functions defined in the script for adding, updating, and managing books and members.

Learning Objectives
-------------------

This project serves as a practical application of my knowledge in Python and MySQL. It covers:

-   **Python Programming**: Demonstrates the use of Python for database operations, including CRUD (Create, Read, Update, Delete) functionalities.
-   **MySQL Database**: Shows how to create and manage a MySQL database and tables from a Python script.
-   **Database Connectivity**: Implements MySQLdb for connecting and executing SQL queries from Python.
-   **Exception Handling**: Uses try-except blocks to handle potential errors during database operations.
