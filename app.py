from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Set your Hardcover API key here or use environment variable
HARDCOVER_API_KEY = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2ZXJzaW9uIjoiNiIsImlkIjoyMDQ4OCwibG9nZ2VkSW4iOnRydWUsInN1YiI6IjIwNDg4IiwiaWF0IjoxNzI5OTUzMDQyLCJleHAiOjE3NjE0MDI5NDIsImh0dHBzOi8vaGFzdXJhLmlvL2p3dC9jbGFpbXMiOnsieC1oYXN1cmEtYWxsb3dlZC1yb2xlcyI6WyJ1c2VyIl0sIngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6InVzZXIiLCJ4LWhhc3VyYS1yb2xlIjoidXNlciIsIlgtaGFzdXJhLXVzZXItaWQiOiIyMDQ4OCJ9fQ.0_CR_HDBOCDlcppUE6Aeiv52bQFNU5Mk6_wQQDys52Y"

# Ensure the API key is prefixed with 'Bearer '
AUTH_HEADER = f'Bearer {HARDCOVER_API_KEY}'
HARDCOVER_API_URL = 'https://api.hardcover.app/v1/graphql'

# Function to make GraphQL request to Hardcover
def make_graphql_request(query):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': AUTH_HEADER,
    }
    response = requests.post(
        HARDCOVER_API_URL,
        json={'query': query},
        headers=headers
    )
    return response.json()

# Flask route to search books by title
@app.route('/search_book', methods=['GET'])
def search_book():
    title = request.args.get('title', 'Dune')  # Default to "Dune" if no title provided
    query = f'''
    {{
      books(
        where: {{title: {{_eq: "{title}"}}}}
      ) {{
        title
        users_read_count
      }}
    }}
    '''
    response = make_graphql_request(query)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
