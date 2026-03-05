# Library Management System (Python + Tkinter + SQLite)

## Overview

This project is a **desktop-based Library Management System** developed using **Python, Tkinter for the graphical user interface, and SQLite for database management**. The system allows users to register, log in, browse available books, borrow and return books, and view their borrowing history.

The application demonstrates the implementation of **database integration, GUI development, authentication systems, and basic library management operations** within a single Python application.

---

## Features

* User registration and login system
* Role selection during registration (Student / Faculty)
* Secure credential validation with username and password rules
* Book catalog management using SQLite database
* View available books and their availability status
* Borrow books from the library
* Return borrowed books
* Track personal borrowing history
* Full-screen graphical user interface
* Background image integration for improved visual design

---

## System Functionalities

### 1. User Registration

Users can create an account by providing:

* Username
* Password
* Role (Student or Faculty)

Validation rules:

* Username must be at least **4 characters** and alphanumeric.
* Password must be at least **6 characters** and contain **both letters and numbers**.

---

### 2. User Login

Registered users can log in using their credentials. After successful authentication, they are redirected to the **dashboard**.

---

### 3. Dashboard

The dashboard provides access to the following features:

* View Books
* Borrow Books
* Return Books
* View Borrowing History
* Logout

---

### 4. View Books

Displays the list of books available in the library along with:

* Total number of copies
* Currently available copies

---

### 5. Borrow Books

Users can select available books and borrow them. The system:

* Records the borrowing date
* Updates the number of available copies
* Stores the transaction in the database

---

### 6. Return Books

Users can return books they previously borrowed. When a book is returned:

* The borrowing record is removed
* The available book count is updated

---

### 7. Borrowing History

Users can view a list of books they currently have borrowed along with the **date of borrowing**.

---

## Technologies Used

* **Python**
* **Tkinter** (Graphical User Interface)
* **SQLite** (Database management)
* **Pillow (PIL)** for image handling
* Regular Expressions for password validation
* Datetime module for tracking borrowing dates

---

## Database Structure

The application uses an SQLite database named **library.db** with the following tables:

### Users Table

| Column   | Description                    |
| -------- | ------------------------------ |
| username | Unique username                |
| password | User password                  |
| role     | User role (student or faculty) |

---

### Books Table

| Column    | Description                |
| --------- | -------------------------- |
| title     | Book title                 |
| total     | Total number of copies     |
| available | Currently available copies |

---

### Borrowed Table

| Column      | Description                     |
| ----------- | ------------------------------- |
| username    | User who borrowed the book      |
| book_title  | Title of borrowed book          |
| borrow_date | Date when the book was borrowed |

---

## Project Structure

```
library-management-system/
│
├── library_system.py
│   Main application source code
│
├── library.db
│   SQLite database storing users and books
│
├── books_bg.png
│   Background image used in the interface
│
└── README.md
    Project documentation
```

---

## Installation Requirements

Ensure that **Python 3.x** is installed on your system.

### Install Required Libraries

Install the required dependencies using pip:

```
pip install pillow
```

Tkinter and SQLite are included by default with most Python installations.

---

## Running the Application

1. Clone the repository

```
git clone https://github.com/your-username/library-management-system.git
```

2. Navigate to the project directory

```
cd library-management-system
```

3. Run the application

```
python library_system.py
```

---

## Key Concepts Demonstrated

This project demonstrates the following programming concepts:

* GUI development using Tkinter
* Database integration using SQLite
* User authentication systems
* Data validation using regular expressions
* CRUD operations (Create, Read, Update, Delete)
* Event-driven programming
* State management within GUI applications

---

## Possible Future Enhancements

Potential improvements for the system include:

* Admin dashboard for managing books and users
* Book search and filtering functionality
* Borrowing limits per user
* Return deadline and fine calculation system
* Email notifications for due dates
* Book reservation feature
* Improved UI with modern themes

---

## Author

Deepthi Busse

Student learning **Data Science, Python programming, and software development through practical projects**.

