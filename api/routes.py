from flask import Blueprint, jsonify, request
import requests

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
