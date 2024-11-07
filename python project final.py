import tkinter as tk
from tkinter import messagebox, simpledialog

# Basic Book Class
class Book:
    def __init__(self, title, author, genre):
        self.title = title
        self.author = author
        self.genre = genre
        self.is_available = True

    def check_availability(self):
        return self.is_available

    def update_availability(self, status):
        self.is_available = status


# Subclasses for Book Types
class Fiction(Book):
    def __init__(self, title, author):
        super().__init__(title, author, "Fiction")


class NonFiction(Book):
    def __init__(self, title, author):
        super().__init__(title, author, "Non-Fiction")


class Reference(Book):
    def __init__(self, title, author):
        super().__init__(title, author, "Reference")


# LibraryCatalog Class to Manage Books
class LibraryCatalog:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        return f"Book '{book.title}' added to the catalog."

    def remove_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                self.books.remove(book)
                return f"Book '{title}' removed from the catalog."
        return f"Book '{title}' not found in the catalog."

    def search_book(self, title=None, author=None):
        results = []
        for book in self.books:
            if (title and book.title.lower() == title.lower()) or (author and book.author.lower() == author.lower()):
                results.append(book)
        return results

    def get_available_books(self):
        return [book for book in self.books if book.is_available]


# Main GUI Application with Customized Dark Mode
class LibraryApp:
    def __init__(self, root):
        self.catalog = LibraryCatalog()
        self.root = root
        self.root.title("Library Catalog System")
        self.root.geometry("500x400")

        # Set modified dark mode colors with light grey buttons
        self.bg_color = "#2e2e2e"  # Dark background color
        self.fg_color = "#ffffff"  # White text color
        self.btn_color = "#d3d3d3" # Light grey button color
        self.root.configure(bg=self.bg_color)

        # Heading Label with bold text
        label_font = ("Arial", 18, "bold")  # Bold font for label
        self.label = tk.Label(root, text="Library Catalog System", font=label_font, bg=self.bg_color, fg=self.fg_color)
        self.label.pack(pady=10)

        # Buttons with bold text
        button_font = ("Arial", 12, "bold")  # Bold font for buttons
        self.add_button = tk.Button(root, text="Add Book", command=self.add_book, bg=self.btn_color, fg=self.bg_color, width=20, font=button_font)
        self.add_button.pack(pady=5)

        self.remove_button = tk.Button(root, text="Remove Book", command=self.remove_book, bg=self.btn_color, fg=self.bg_color, width=20, font=button_font)
        self.remove_button.pack(pady=5)

        self.search_button = tk.Button(root, text="Search Book", command=self.search_book, bg=self.btn_color, fg=self.bg_color, width=20, font=button_font)
        self.search_button.pack(pady=5)

        self.display_button = tk.Button(root, text="Display Available Books", command=self.display_available_books, bg=self.btn_color, fg=self.bg_color, width=20, font=button_font)
        self.display_button.pack(pady=5)

        self.borrow_button = tk.Button(root, text="Borrow Book", command=self.borrow_book, bg=self.btn_color, fg=self.bg_color, width=20, font=button_font)
        self.borrow_button.pack(pady=5)

        self.return_button = tk.Button(root, text="Return Book", command=self.return_book, bg=self.btn_color, fg=self.bg_color, width=20, font=button_font)
        self.return_button.pack(pady=5)

    def add_book(self):
        title = simpledialog.askstring("Add Book", "Enter book title:", parent=self.root)
        author = simpledialog.askstring("Add Book", "Enter author:", parent=self.root)
        genre = simpledialog.askstring("Add Book", "Enter genre (Fiction/Non-Fiction/Reference):", parent=self.root)

        if genre.lower() == "fiction":
            book = Fiction(title, author)
        elif genre.lower() == "non-fiction":
            book = NonFiction(title, author)
        elif genre.lower() == "reference":
            book = Reference(title, author)
        else:
            messagebox.showerror("Error", "Invalid genre. Please enter Fiction, Non-Fiction, or Reference.")
            return

        message = self.catalog.add_book(book)
        messagebox.showinfo("Success", message, parent=self.root)

    def remove_book(self):
        title = simpledialog.askstring("Remove Book", "Enter book title to remove:", parent=self.root)
        message = self.catalog.remove_book(title)
        messagebox.showinfo("Result", message, parent=self.root)

    def search_book(self):
        title = simpledialog.askstring("Search Book", "Enter book title to search:", parent=self.root)
        author = simpledialog.askstring("Search Book", "Enter author (leave blank if searching by title):", parent=self.root)

        results = self.catalog.search_book(title=title, author=author)
        if results:
            result_text = "\n".join([f"Title: {book.title}, Author: {book.author}, Genre: {book.genre}, "
                                     f"Status: {'Available' if book.is_available else 'Not Available'}"
                                     for book in results])
            messagebox.showinfo("Search Results", result_text, parent=self.root)
        else:
            messagebox.showinfo("Search Results", "No matching books found.", parent=self.root)

    def display_available_books(self):
        available_books = self.catalog.get_available_books()
        if available_books:
            books_text = "\n".join([f"Title: {book.title}, Author: {book.author}, Genre: {book.genre}" for book in available_books])
            messagebox.showinfo("Available Books", books_text, parent=self.root)
        else:
            messagebox.showinfo("Available Books", "No books currently available.", parent=self.root)

    def borrow_book(self):
        title = simpledialog.askstring("Borrow Book", "Enter book title to borrow:", parent=self.root)
        results = self.catalog.search_book(title=title)

        if results:
            book = results[0]
            if book.check_availability():
                book.update_availability(False)
                messagebox.showinfo("Success", f"You have borrowed '{book.title}'.", parent=self.root)
            else:
                messagebox.showinfo("Unavailable", f"'{book.title}' is currently not available.", parent=self.root)
        else:
            messagebox.showinfo("Not Found", "Book not found.", parent=self.root)

    def return_book(self):
        title = simpledialog.askstring("Return Book", "Enter book title to return:", parent=self.root)
        results = self.catalog.search_book(title=title)

        if results:
            book = results[0]
            book.update_availability(True)
            messagebox.showinfo("Success", f"You have returned '{book.title}'.", parent=self.root)
        else:
            messagebox.showinfo("Not Found", "Book not found.", parent=self.root)


# Run the application
root = tk.Tk()
app = LibraryApp(root)
root.mainloop()
