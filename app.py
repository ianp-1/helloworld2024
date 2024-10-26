from flask import Flask, jsonify
import requests

app = Flask(__name__)

GRAPHQL_URL = "https://api.hardcover.app/v1/graphql"
AUTH_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2ZXJzaW9uIjoiNiIsImlkIjoyMDQ4NywibG9nZ2VkSW4iOnRydWUsInN1YiI6IjIwNDg3IiwiaWF0IjoxNzI5OTUyODA2LCJleHAiOjE3NjE0MDI3MDYsImh0dHBzOi8vaGFzdXJhLmlvL2p3dC9jbGFpbXMiOnsieC1oYXN1cmEtYWxsb3dlZC1yb2xlcyI6WyJ1c2VyIl0sIngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6InVzZXIiLCJ4LWhhc3VyYS1yb2xlIjoidXNlciIsIlgtaGFzdXJhLXVzZXItaWQiOiIyMDQ4NyJ9fQ.4ZFEMUBXW7HIBnyLn6GBvnIHF560knttRITM36_xUpA"

@app.route('/', methods=['GET'])
#def googlevision():
    # get book name
    # book_name, author_name
def bookInfo():
    title = "Dune"
    query = f"""
        {{
            books (
                order_by: {{users_read_count: desc}}
                where: {{title: {{_eq: "{title}"}}}}
                limit: 5
            ) {{
                users_read_count
                title
            }}
        }}
    """  
    
    headers = {
        "Authorization": AUTH_TOKEN,
        "Content-Type": "application/json"
    }
    
    response = requests.post(GRAPHQL_URL, json={'query': query}, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Request failed", "status_code": response.status_code}), response.status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)