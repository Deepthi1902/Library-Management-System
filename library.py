import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import datetime
import re

# Theme Constants
PRIMARY_BG = "#d0e6f7"
BUTTON_BG = "#ffffff"
BUTTON_FG = "#003366"
FONT_TITLE = ("Arial", 20, "bold")
FONT_SUB = ("Arial", 16, "bold")
FONT_LABEL = ("Arial", 12, "bold")
FONT_TEXT = ("Arial", 12)

# SQLite setup
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY, password TEXT, role TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS books (
    title TEXT PRIMARY KEY, total INTEGER, available INTEGER)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS borrowed (
    username TEXT, book_title TEXT, borrow_date TEXT, PRIMARY KEY (username, book_title))''')

# Add default books
default_books = {
    'Python Basics': 2, 'Data Science': 2, 'Algorithms': 1,
    'Database Systems': 1, 'AI Fundamentals': 1, 'Networking': 1,
    'Machine Learning': 1, 'Operating Systems': 1,
    'Cyber Security': 1, 'Web Development': 1
}
for title, qty in default_books.items():
    cursor.execute("INSERT OR IGNORE INTO books VALUES (?, ?, ?)", (title, qty, qty))
conn.commit()

# GUI setup
root = tk.Tk()
root.title("Library System")
root.attributes('-fullscreen', True)
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

# Load background image
bg_img = Image.open("books_bg.png")
bg_img = bg_img.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_img)
background_label = tk.Label(root, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

current_user = {"username": None, "role": None}

def clear_window():
    for widget in root.winfo_children():
        if widget != background_label:
            widget.destroy()

def back_button(cmd):
    tk.Button(root, text="Back", command=cmd, font=FONT_LABEL, bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=10)

def labeled_entry(label):
    tk.Label(root, text=label, font=FONT_LABEL, bg=PRIMARY_BG, fg=BUTTON_FG).pack(pady=5)
    entry = tk.Entry(root, font=FONT_TEXT, bg="#ffffff", fg="#000000")
    entry.pack(pady=5)
    return entry

def is_valid_username(username): return len(username) >= 4 and username.isalnum()
def is_valid_password(password): return len(password) >= 6 and re.search(r"[A-Za-z]", password) and re.search(r"[0-9]", password)

def print_all_credentials():
    print("\n--- Registered Users ---")
    cursor.execute("SELECT username, password FROM users")
    for u, p in cursor.fetchall(): print(f"Username: {u} | Password: {p}")
    print("------------------------\n")

def register_screen():
    clear_window()
    tk.Label(root, text="Register", font=FONT_SUB, bg=PRIMARY_BG, fg=BUTTON_FG).pack(pady=10)
    username = labeled_entry("Username")
    password = labeled_entry("Password")
    password.config(show="*")

    tk.Label(root, text="Role (student/faculty)", font=FONT_LABEL, bg=PRIMARY_BG, fg=BUTTON_FG).pack()
    role_var = tk.StringVar()
    role_var.set("student")
    role_menu = ttk.Combobox(root, textvariable=role_var, values=["student", "faculty"], state="readonly", font=FONT_TEXT)
    role_menu.pack(pady=5)

    def register():
        u, p, r = username.get(), password.get(), role_var.get().lower()
        if not is_valid_username(u):
            messagebox.showerror("Error", "Username must be 4+ characters and alphanumeric")
        elif not is_valid_password(p):
            messagebox.showerror("Error", "Password must be 6+ characters, with letters and numbers")
        else:
            try:
                cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (u, p, r))
                conn.commit()
                messagebox.showinfo("Success", "Registered successfully!")
                print_all_credentials()
                login_screen()
            except:
                messagebox.showerror("Error", "User already exists")

    tk.Button(root, text="Register", command=register, font=FONT_LABEL, bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=10)
    back_button(main_menu)

def login_screen():
    clear_window()
    tk.Label(root, text="Login", font=FONT_SUB, bg=PRIMARY_BG, fg=BUTTON_FG).pack(pady=10)
    username = labeled_entry("Username")
    password = labeled_entry("Password")
    password.config(show="*")

    def login():
        u, p = username.get(), password.get()
        cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (u, p))
        result = cursor.fetchone()
        if result:
            current_user["username"], current_user["role"] = u, result[0]
            dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    tk.Button(root, text="Login", command=login, font=FONT_LABEL, bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=10)
    back_button(main_menu)

def dashboard():
    clear_window()
    tk.Label(root, text=f"Welcome {current_user['username']}!", font=FONT_SUB, bg=PRIMARY_BG, fg=BUTTON_FG).pack(pady=10)
    for text, cmd in [("View Books", view_books), ("Borrow Books", borrow_book),
                      ("Return Books", return_book), ("View Borrowing History", view_history)]:
        tk.Button(root, text=text, width=20, command=cmd, font=FONT_LABEL, bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=5)
    tk.Button(root, text="Logout", width=20, command=main_menu, font=FONT_LABEL, bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=20)

def view_books():
    clear_window()
    tk.Label(root, text="Available Books", font=FONT_SUB, bg=PRIMARY_BG, fg=BUTTON_FG).pack(pady=10)
    cursor.execute("SELECT * FROM books")
    for title, total, available in cursor.fetchall():
        tk.Label(root, text=f"{title}: {available}/{total}", font=FONT_TEXT, bg=PRIMARY_BG, fg=BUTTON_FG).pack()
    back_button(dashboard)

def borrow_book():
    clear_window()
    tk.Label(root, text="Select Books to Borrow", font=FONT_SUB, bg=PRIMARY_BG, fg=BUTTON_FG).pack(pady=10)
    cursor.execute("SELECT title FROM books WHERE available > 0")
    books = [r[0] for r in cursor.fetchall()]

    if not books:
        tk.Label(root, text="No books available", font=FONT_TEXT, bg=PRIMARY_BG, fg=BUTTON_FG).pack()
        back_button(dashboard)
        return

    selected_books = []
    for b in books:
        var = tk.BooleanVar()
        tk.Checkbutton(root, text=b, variable=var, font=FONT_TEXT, bg=PRIMARY_BG, fg=BUTTON_FG).pack(anchor='w', padx=50)
        selected_books.append((b, var))

    def borrow():
        for title, var in selected_books:
            if var.get():
                cursor.execute("INSERT INTO borrowed (username, book_title, borrow_date) VALUES (?, ?, ?)",
                               (current_user["username"], title, datetime.datetime.now().isoformat()))
                cursor.execute("UPDATE books SET available = available - 1 WHERE title = ?", (title,))
        conn.commit()
        messagebox.showinfo("Success", "Books borrowed successfully!")
        dashboard()

    tk.Button(root, text="Borrow", command=borrow, font=FONT_LABEL, bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=10)
    back_button(dashboard)

def return_book():
    clear_window()
    cursor.execute("SELECT book_title FROM borrowed WHERE username=?", (current_user["username"],))
    books = cursor.fetchall()
    if not books:
        tk.Label(root, text="No books to return.", font=FONT_TEXT, bg=PRIMARY_BG, fg=BUTTON_FG).pack(pady=10)
    else:
        for book in books:
            title = book[0]
            tk.Label(root, text=f"Returning: {title}", font=("Arial", 14, "bold"), bg=PRIMARY_BG, fg=BUTTON_FG).pack(pady=10)
            def return_b():
                cursor.execute("DELETE FROM borrowed WHERE username=? AND book_title=?", 
                               (current_user["username"], title))
                cursor.execute("UPDATE books SET available = available + 1 WHERE title=?", (title,))
                conn.commit()
                messagebox.showinfo("Returned", f"Returned '{title}' successfully")
                dashboard()
            tk.Button(root, text="Return", command=return_b, font=FONT_LABEL, bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=10)
    back_button(dashboard)

def view_history():
    clear_window()
    tk.Label(root, text="Borrowing History", font=FONT_SUB, bg=PRIMARY_BG, fg=BUTTON_FG).pack(pady=10)
    cursor.execute("SELECT book_title, borrow_date FROM borrowed WHERE username=?", (current_user["username"],))
    for book, borrow_date in cursor.fetchall():
        tk.Label(root, text=f"{book} - Borrowed on: {borrow_date}", font=FONT_TEXT, bg=PRIMARY_BG, fg=BUTTON_FG).pack()
    back_button(dashboard)

def main_menu():
    clear_window()
    tk.Label(root, text="Library System", font=FONT_TITLE, bg=PRIMARY_BG, fg=BUTTON_FG).pack(pady=20)
    for text, cmd in [("Login", login_screen), ("Register", register_screen)]:
        tk.Button(root, text=text, width=20, command=cmd, font=FONT_LABEL, bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=5)
    tk.Button(root, text="Exit", width=20, command=root.quit, font=FONT_LABEL, bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=20)

# Start the application with the main menu
main_menu()

# Main loop to run the tkinter app
root.mainloop()
