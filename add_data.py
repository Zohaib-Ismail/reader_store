import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QComboBox, QMessageBox
)
from models import add_book, update_book, get_book_by_id


class BookManager(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Book Manager")
        self.layout = QVBoxLayout()

        # Dropdown for selecting a book
        self.book_combo = QComboBox(self)
        self.book_combo.addItem("Select a book to edit")
        self.layout.addWidget(self.book_combo)
        self.load_books()
        self.book_combo.currentIndexChanged.connect(self.load_book)

        # Input fields
        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("Enter book title")
        self.layout.addWidget(self.title_input)

        self.author_input = QLineEdit(self)
        self.author_input.setPlaceholderText("Enter book author")
        self.layout.addWidget(self.author_input)

        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText("Enter description")
        self.layout.addWidget(self.description_input)

        self.genre_input = QLineEdit(self)
        self.genre_input.setPlaceholderText("Enter genre")
        self.layout.addWidget(self.genre_input)

        self.epub_input = QLineEdit(self)
        self.epub_input.setPlaceholderText("Select EPUB file")
        self.layout.addWidget(self.epub_input)

        self.cover_input = QLineEdit(self)
        self.cover_input.setPlaceholderText("Select cover image")
        self.layout.addWidget(self.cover_input)

        # Buttons for adding and updating books
        self.add_book_button = QPushButton("Add New Book", self)
        self.add_book_button.clicked.connect(self.add_new_book)
        self.layout.addWidget(self.add_book_button)

        self.update_book_button = QPushButton("Update Selected Book", self)
        self.update_book_button.clicked.connect(self.update_book)
        self.layout.addWidget(self.update_book_button)

        self.setLayout(self.layout)

    def load_books(self):
        """Load all books from the database into the ComboBox."""
        self.book_combo.clear()
        self.book_combo.addItem("Select a book to edit")
        conn = sqlite3.connect("books.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM books")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            book_id, title = row
            self.book_combo.addItem(title, book_id)

    def load_book(self):
        """Load details of the selected book into input fields."""
        book_id = self.book_combo.currentData()
        if book_id:
            book = get_book_by_id(book_id)
            if book:
                self.title_input.setText(book["title"])
                self.author_input.setText(book["author"])
                self.description_input.setText(book["description"])
                # Ensure genre is handled even if it is empty or None
                self.genre_input.setText(book.get("genre", ""))  # Default to empty string if None
                self.epub_input.setText(book["epub_path"])
                self.cover_input.setText(book["cover_image_path"])
            else:
                QMessageBox.warning(self, "Error", "Book not found!")

    def add_new_book(self):
        """Add a new book to the database."""
        title = self.title_input.text()
        author = self.author_input.text()
        description = self.description_input.text()
        genre = self.genre_input.text()  # Get the genre input
        epub_path = self.epub_input.text()
        cover_image_path = self.cover_input.text()

        if title and author and description and genre and epub_path and cover_image_path:
            add_book(title, author, description, genre, epub_path, cover_image_path)  # Pass genre to the add_book function
            QMessageBox.information(self, "Success", "Book added successfully!")
            self.load_books()
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "Error", "All fields are required!")

    def update_book(self):
        """Update details of the selected book."""
        book_id = self.book_combo.currentData()
        if not book_id:
            QMessageBox.warning(self, "Error", "Please select a book to update.")
            return

        title = self.title_input.text()
        author = self.author_input.text()
        description = self.description_input.text()
        genre = self.genre_input.text()  # Get the genre input
        epub_path = self.epub_input.text()
        cover_image_path = self.cover_input.text()

        if title and author and description and genre and epub_path and cover_image_path:
            update_book(book_id, title, author, description, genre, epub_path, cover_image_path)  # Pass genre to the update_book function
            QMessageBox.information(self, "Success", "Book updated successfully!")
            self.load_books()
        else:
            QMessageBox.warning(self, "Error", "All fields are required!")

    def clear_inputs(self):
        """Clear all input fields."""
        self.title_input.clear()
        self.author_input.clear()
        self.description_input.clear()
        self.genre_input.clear()  # Clear the genre field
        self.epub_input.clear()
        self.cover_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    manager = BookManager()
    manager.show()
    sys.exit(app.exec_())
