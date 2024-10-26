from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OPEN_LIBRARY_API_URL = 'https://openlibrary.org/search.json'

# Function to make a request to the Open Library API
def search_books(query, page=1):
    search_url = f"{OPEN_LIBRARY_API_URL}?q={query}&page={page}"
    response = requests.get(search_url)
    return response.json()

# Flask route to search books by title or author
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')  # Get the query parameter
    page = request.args.get('page', 1)  # Get the page parameter (default to 1)

    if not query:
        return jsonify({"error": "Please provide a search query."}), 400

    # Search for books using the Open Library API
    results = search_books(query, page)
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
