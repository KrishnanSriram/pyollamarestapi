from flask import Blueprint, jsonify, request
import requests
import os

# Define the Blueprint
api_blueprint = Blueprint('api', __name__)

# Route for /api
@api_blueprint.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the API Home"}), 200

# Route for /api/about
@api_blueprint.route('/about', methods=['GET'])
def about():
    return jsonify({"message": "About the API"}), 200

# Route for /api/query
@api_blueprint.route('/query', methods=['POST'])
def query():
    # Step 1: Validate input data
    data, error = validate_input(request)
    if error:
        return error

    # Step 2: Make external API call
    external_response, error = call_external_api(model=data['model'], prompt=data['prompt'])
    if error:
        return error

    # Step 3: Return assembled response
    return assemble_response(model= data['model'], prompt = data['prompt'], external_response=external_response)

# New Route for /api/upload to handle PDF uploads
@api_blueprint.route('/upload', methods=['POST'])
def upload_pdf():
    # Check if a file is part of the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    # Check if the file has a valid PDF filename
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "File must be a PDF"}), 400

    # Save the file to the designated directory
    file_path = os.path.join("./pdfs", file.filename)
    file.save(file_path)

    return jsonify({"message": f"File '{file.filename}' uploaded successfully"}), 200

def validate_input(request):
    """Validate incoming JSON data for 'model' and 'prompt'."""
    if not request.is_json:
        return None, jsonify({"error": "Request body must be JSON"}), 400

    data = request.get_json()
    model = data.get('model')
    prompt = data.get('prompt')

    if not model or not prompt:
        return None, jsonify({"error": "Both 'model' and 'prompt' must be provided"}), 400

    return data, None


def call_external_api(model, prompt):
    """Call an external API with the given model and prompt."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        response.raise_for_status()
        return response.json(), None

    except requests.RequestException as e:
        return None, jsonify({"error": f"Failed to connect to external API: {e}"}), 500


def assemble_response(model, prompt, external_response):
    """Assemble and return the API response."""
    return jsonify({
        "model": model,
        "prompt": prompt,
        "body": external_response
    }), 200
