import sqlite3

# Function to add a new book
def add_book(title, author, description, genre, epub_path, cover_image_path):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO books (title, author, description, genre, epub_path, cover_image_path)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, author, description, genre, epub_path, cover_image_path))
    conn.commit()
    conn.close()

# Function to update an existing book
def update_book(book_id, title, author, description, epub_path, cover_image_path):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE books
        SET title = ?, author = ?, description = ?, epub_path = ?, cover_image_path = ?
        WHERE id = ?
    ''', (title, author, description, epub_path, cover_image_path, book_id))
    conn.commit()
    conn.close()

# Function to fetch a book by ID
def get_book_by_id(book_id):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "description": row[3],
            "epub_path": row[4],
            "cover_image_path": row[5],
        }
    return None

# Utility to create the books table (if it doesn't exist already)
def initialize_db():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            description TEXT,
            epub_path TEXT NOT NULL,
            cover_image_path TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
