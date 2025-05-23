from flask import Flask, jsonify, render_template, request
import json

app = Flask(__name__)

# Define the path to your JSON file
JSON_FILE = 'data.json'

def read_json_file():
    try:
        with open(JSON_FILE, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return []

def write_json_file(data):
    with open(JSON_FILE, 'w') as file:
        json.dump(data, file, indent=2)

@app.route('/api/books', methods=['GET'])
def get_all_books():
    try:
        books = read_json_file()

        return jsonify({'books': books})
    except Exception as e:
        return jsonify({'error': str(e)})

# API to add a book to the JSON file
@app.route('/api/add_book', methods=['POST'])
def add_book():
    try:
        # Get book details from the request
        data = request.get_json()
        title = data.get('title')
        publication_year = data.get('publication_year')

        # Read existing data from the JSON file
        books = read_json_file()

        # Add the new book to the list
        book = {
            'title': title,
            'publication_year': publication_year
            # Add other attributes here as needed
        }
        books.append(book)

        # Write the updated data back to the JSON file
        write_json_file(books)

        return jsonify({'message': 'Book added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

# Route to render the index.html page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index2.html')
def index2():
    return render_template('index2.html')


@app.route('/index3.html')
def index3():
    return render_template('index3.html')



@app.route('/api/search_books', methods=['POST'])
def search_books():
    try:
        search_text = request.get_json().get('search_text', '')
        books = read_json_file()

        # Filter books based on search text
        matching_books = [book for book in books if search_text.lower() in book['title'].lower()]

        return jsonify({'books': matching_books})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
