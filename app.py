from flask import Flask, render_template, request
import sqlite3
import random  # Import random module to pick random books

app = Flask(__name__)

# Connect to your SQLite database and fetch books grouped by genre
def get_books_by_genre():
    connection = sqlite3.connect('books.db')  # Replace with the actual path of your DB
    cursor = connection.cursor()

    # Fetch all distinct genres
    cursor.execute('SELECT DISTINCT genre FROM books')
    genres = cursor.fetchall()

    # Create a dictionary to hold genres and their respective books
    books_by_genre = {}
    for genre in genres:
        cursor.execute('SELECT * FROM books WHERE genre = ?', (genre[0],))
        books = cursor.fetchall()
        books_by_genre[genre[0]] = books

    connection.close()
    return books_by_genre

# Fetch all books from the database and pick a few random ones
def get_random_books():
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    
    # Fetch all books
    cursor.execute('SELECT * FROM books')
    all_books = cursor.fetchall()
    
    # Pick 5 random books
    random_books = random.sample(all_books, 5)  # Change the number to adjust how many random books
    connection.close()
    
    return random_books

# Get books for a specific genre
def get_books_for_genre(genre):
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM books WHERE genre = ?', (genre,))
    books = cursor.fetchall()
    connection.close()
    return books

# Search books by keyword (title, genre, etc.)
def search_books(query):
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    # Search for books where the title or genre matches the query (case-insensitive)
    query = f"%{query}%"
    print(f"Executing SQL query: SELECT * FROM books WHERE title LIKE '{query}' OR genre LIKE '{query}'")  # Debugging the SQL query
    cursor.execute('SELECT * FROM books WHERE title LIKE ? OR genre LIKE ?', (query, query))
    results = cursor.fetchall()
    connection.close()
    return results

@app.route('/')
def index():
    books_by_genre = get_books_by_genre()  # Get books grouped by genre
    featured_books = get_random_books()  # Get a few random books for the featured banner
    return render_template('index.html', books_by_genre=books_by_genre, featured_books=featured_books)

@app.route('/genres')
def genres():
    genres = get_books_by_genre()  # Get genres from the database
    return render_template('genres.html', genres=genres)

@app.route('/genre/<genre_name>')
def genre(genre_name):
    books = get_books_for_genre(genre_name)  # Get books of the selected genre
    return render_template('genre.html', genre_name=genre_name, books=books)

@app.route('/book/<int:book_id>')
def book_details(book_id):
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()
    
    # Fetch 5 random books for the "More Books" section
    random_books = get_random_books()
    
    connection.close()
    
    return render_template('details.html', book=book, random_books=random_books)


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')  # Get the search query from URL parameters
    print(f"Search Query: {query}")  # Debugging line to show query
    results = search_books(query)  # Query the database for matching books
    return render_template('search_results.html', query=query, results=results)



if __name__ == '__main__':
    app.run(debug=True)
