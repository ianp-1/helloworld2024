from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
from typing_extensions import override
from openai import AssistantEventHandler
import requests
import json
import os
from paddleocr import PaddleOCR

# Load environment variables
load_dotenv()

# OpenAI and Open Library configuration
OPEN_LIBRARY_SEARCH_URL = 'https://openlibrary.org/search.json'

assistantID = "asst_Eexxahpbuh67V4i0Rob9m16Z"
apiKey = os.getenv('OPENAI_API_KEY')

client = OpenAI(
    api_key=apiKey,
    organization='org-FC57og8jDQ11tBkrgIgFX6hB',
    project='proj_0j12yDVX33RfyR5xcnspR60p',
)

app = Flask(__name__)
CORS(app)

# Initialize PaddleOCR
ocr_model = PaddleOCR(use_angle_cls=True, lang='en')  # Adjust language as needed

# Function to perform OCR using PaddleOCR
def ocr_image(image_path):
    try:
        # Perform OCR on the image
        result = ocr_model.ocr(image_path, cls=True)
        
        # Extract detected text from PaddleOCR results
        text = ''
        for line in result:
            for word_info in line:
                text += word_info[1][0] + ' '
                
        return text.strip()
    except Exception as e:
        return str(e)

# Define the custom EventHandler class for streaming
class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)

    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)

# Function to clean up the OCR text using OpenAI and parse JSON response
def clean_text_with_openai(text):
    # Create a new thread
    thread = client.beta.threads.create()

    # Send the initial message to the assistant
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=text,
    )

    # Stream the response using the EventHandler class
    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistantID,
        event_handler=EventHandler(),
    ) as stream:
        stream.until_done()

    # Retrieve the messages in the thread
    messages = client.beta.threads.messages.list(thread_id=thread.id)

    # Find the assistant's response
    assistant_message = None
    for message in messages:
        if message.role == 'assistant':
            assistant_message = message
            break

    if not assistant_message:
        return {"error": "Assistant response not found"}

    # Extract the JSON content from the assistant's response
    response_json = None
    for content_part in assistant_message.content:
        if content_part.type == 'text':
            try:
                response_json = json.loads(content_part.text.value)
                break
            except json.JSONDecodeError:
                return {"error": "Failed to decode JSON from assistant response"}

    # Validate the parsed JSON structure
    if response_json and "books" in response_json:
        return response_json["books"]
    else:
        return {"error": "Invalid response schema"}

# Function to search Open Library using title and author
def search_open_library(title, author):
    params = {'title': title, 'title_exact': 'true', 'sort': 'rating', 'limit': 3}
    response = requests.get(OPEN_LIBRARY_SEARCH_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data from Open Library"}

# Flask route to process an image and return book info
@app.route('/process-image', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded image temporarily
    image_path = os.path.join('/tmp', file.filename)
    file.save(image_path)

    # Perform OCR using PaddleOCR
    extracted_text = ocr_image(image_path)
    if not extracted_text:
        return jsonify({"error": "Could not extract text from image"}), 500

    # Clean up the extracted text using OpenAI and parse the JSON response
    cleaned_books = clean_text_with_openai(extracted_text)
    if "error" in cleaned_books:
        return jsonify({"error": cleaned_books["error"]}), 500

    # Iterate over each book and search Open Library
    books_info = []
    for book in cleaned_books:
        title = book.get('title', '')
        author = book.get('author', '')

        # Search Open Library using the cleaned title and author
        search_results = search_open_library(title, author)

        # Extract relevant book data from results
        books = []
        for doc in search_results.get('docs', []):
            book_info = {
                'title': doc.get('title'),
                'author': doc.get('author_name', []),
                'first_publish_year': doc.get('first_publish_year'),
                'cover_id': doc.get('cover_i'),
                'first_sentence': doc.get('first_sentence', ['N/A'])[0]
            }
            books.append(book_info)

        books_info.append({
            "extracted_title": title,
            "extracted_author": author,
            "books": books
        })

    return jsonify({
        "extracted_text": extracted_text,
        "books_info": books_info
    })


if __name__ == "__main__":
    app.run(debug=True)
