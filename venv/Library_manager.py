import sqlite3
import datetime
import tkinter as tk
from tkinter import ttk

# Connect to the database. This will create a new file named "library.db"
conn = sqlite3.connect('library.db')
c = conn.cursor()

# Create tables
try:
    # Create tables
    c.execute('''CREATE TABLE Books 
                 (id INTEGER PRIMARY KEY, title TEXT, author_id INTEGER, available INTEGER)''')

    c.execute('''CREATE TABLE Authors 
                 (id INTEGER PRIMARY KEY, name TEXT)''')

    c.execute('''CREATE TABLE Borrowers 
                 (id INTEGER PRIMARY KEY, name TEXT)''')

    c.execute('''CREATE TABLE Transactions 
                 (id INTEGER PRIMARY KEY, book_id INTEGER, borrower_id INTEGER, due_date TEXT)''')
except sqlite3.OperationalError:
    pass  # Table already exists, so pass

# Commit the changes and close the connection
conn.commit()
conn.close()


def add_book(title, author_id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("INSERT INTO Books (title, author_id, available) VALUES (?, ?, 1)", (title, author_id))
    conn.commit()
    conn.close()

def add_author(name):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("INSERT INTO Authors (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def add_borrower(name):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("INSERT INTO Borrowers (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()



#Functions for a Users

def check_out_book(book_id, borrower_id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    
    # Set the due date for two weeks from today
    due_date = datetime.datetime.now() + datetime.timedelta(weeks=2)
    due_date_str = due_date.strftime('%Y-%m-%d')
    
    c.execute("INSERT INTO Transactions (book_id, borrower_id, due_date, is_reserved) VALUES (?, ?, ?)", 
              (book_id, borrower_id, due_date_str))
    
    # Mark book as unavailable
    c.execute("UPDATE Books SET available = 0 WHERE id = ?", (book_id,))
    
    conn.commit()
    conn.close()

def return_book(book_id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    
    c.execute("DELETE FROM Transactions WHERE book_id = ?", (book_id,))
    c.execute("UPDATE Books SET available = 1 WHERE id = ?", (book_id,))
    
    conn.commit()
    conn.close()


def reserve_book(book_id, borrower_id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    
    # Check if the book is already reserved or checked out
    c.execute("SELECT * FROM Transactions WHERE book_id = ?", (book_id,))
    transaction = c.fetchone()
    if transaction:
        conn.close()
        return "The book is already reserved or checked out."
    
    # Reserve the book with no due date
    c.execute("INSERT INTO Transactions (book_id, borrower_id, due_date, is_reserved) VALUES (?, ?, NULL, 1)", 
              (book_id, borrower_id))
    
    # Mark book as unavailable in the Books table
    c.execute("UPDATE Books SET available = 0 WHERE id = ?", (book_id,))
    
    conn.commit()
    conn.close()
    return "Book reserved successfully."


#let's Querying!

def list_all_books():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute("SELECT * FROM Books" )
    books = c.fetchall()

    conn.close
    return books

def list_all_authors():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Authors")
    authors = c.fetchall()
    conn.close()
    return authors

def list_all_borrowers():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Borrowers")
    borrowers = c.fetchall()
    conn.close()
    return borrowers


def list_all_transactions():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''SELECT t.id, b.title, bo.name, t.due_date, t.is_reserved 
                 FROM Transactions t 
                 JOIN Books b ON t.book_id = b.id 
                 JOIN Borrowers bo ON t.borrower_id = bo.id''')
    transactions = c.fetchall()
    conn.close()
    return transactions


# Displaying data on tabular format


def display_all_books():
    books = list_all_books()
    print("\nAll Books:")
    print("ID\tTitle\tAuthor ID\tAvailable")
    for book in books:
        print(f"{book[0]}\t{book[1]}\t{book[2]}\t{'Yes' if book[3] else 'No'}")


def display_all_authors():
    authors = list_all_authors()
    print("\nAll Authors:")
    print("ID\tName")
    for author in authors:
        print(f"{author[0]}\t{author[1]}")



def display_all_borrowers():
    borrowers = list_all_borrowers
    print("\nAll Borrowers")
    print("ID\tName")
    for borrower in borrowers:
        print(f"{borrower[0]}\t{borrower[1]}")


def display_all_transactions():
    transactions = list_all_transactions()
    print("\nAll Transactions:")
    print("Trans. ID\tBook Title\tBorrower Name\tDue Date\tReserved")
    for transaction in transactions:
        print(f"{transaction[0]}\t{transaction[1]}\t{transaction[2]}\t{transaction[3]}\t{'Yes' if transaction[4] else 'No'}")


def gui_list_all_books():
    # Create the main window
    root = tk.Tk()
    root.title('All Books')

    # Create a Treeview widget
    tree = ttk.Treeview(root, columns=('ID', 'Title', 'Author ID', 'Available'), show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Title', text='Title')
    tree.heading('Author ID', text='Author ID')
    tree.heading('Available', text='Available')
    tree.pack(padx=20, pady=20)

    # Fetch and insert books data into the Treeview
    books = list_all_books()
    for book in books:
        tree.insert('', 'end', values=(book[0], book[1], book[2], 'Yes' if book[3] else 'No'))

    root.mainloop()




# Sample data
def add_sample_data():
    add_author("J.K. Rowling")
    add_author("George Orwell")
    add_author("J.R.R. Tolkien")
    add_book("Harry Potter and the Philosopher's Stone", 1)  # 1 is the ID of J.K. Rowling
    add_book("1984", 2)  # 2 is the ID of George Orwell
    add_book("The Hobbit", 3)  # 3 is the ID of J.R.R. Tolkien
    add_borrower("John Doe")
    add_borrower("Jane Smith")

# Add the sample data
add_sample_data()

if __name__ == "__main__":
    gui_list_all_books()



 