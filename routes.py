from flask import Blueprint, request, jsonify
from models import snippets, users
from encryption import encrypt_code, decrypt_code
from authentication import hash_password, check_password

# Define Blueprints
snippet_routes = Blueprint('snippet_routes', __name__)
user_routes = Blueprint('user_routes', __name__)

# POST /snippets - Create a new snippet
@snippet_routes.route('/snippets', methods=['POST'])
def create_snippet():
    data = request.get_json()

    # Encrypt the snippet code before saving
    encrypted_code = encrypt_code(data['code'])

    # Generate a new ID (simple way, can be improved)
    snippet_id = len(snippets) + 1

    # Create a new snippet
    snippet = {
        'id': snippet_id,
        'language': data['language'],
        'code': encrypted_code
    }

    # Save to in-memory data store
    snippets.append(snippet)

    return jsonify(snippet), 201

# GET /snippets - Retrieve all snippets
@snippet_routes.route('/snippets', methods=['GET'])
def get_all_snippets():
    # Decrypt the code of each snippet before returning
    decrypted_snippets = [
        {**snippet, 'code': decrypt_code(snippet['code'])} for snippet in snippets
    ]
    return jsonify(decrypted_snippets)

# GET /snippets/<id> - Retrieve a snippet by ID
@snippet_routes.route('/snippets/<int:id>', methods=['GET'])
def get_snippet(id):
    snippet = next((snippet for snippet in snippets if snippet['id'] == id), None)

    if not snippet:
        return jsonify({'error': 'Snippet not found'}), 404

    # Decrypt the code before returning
    snippet['code'] = decrypt_code(snippet['code'])
    return jsonify(snippet)

# GET /snippets?lang=python - Retrieve all snippets of a specific language
@snippet_routes.route('/snippets', methods=['GET'])
def get_snippets_by_language():
    lang = request.args.get('lang')
    filtered_snippets = [snippet for snippet in snippets if snippet['language'].lower() == lang.lower()]

    if not filtered_snippets:
        return jsonify({'error': 'No snippets found for this language'}), 404

    # Decrypt the code before returning
    decrypted_snippets = [
        {**snippet, 'code': decrypt_code(snippet['code'])} for snippet in filtered_snippets
    ]
    return jsonify(decrypted_snippets)

# POST /user - Create a new user
@user_routes.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = hash_password(data['password'])

    user_id = len(users) + 1  # Generate a new ID
    user = {
        'id': user_id,
        'email': data['email'],
        'password': hashed_password
    }

    users.append(user)
    return jsonify({'message': 'User created successfully'}), 201

# GET /user - Retrieve user details (protected endpoint)
@user_routes.route('/user', methods=['GET'])
def get_user():
    auth = request.authorization
    if not auth or not check_password(auth.username, auth.password):
        return jsonify({'error': 'Unauthorized'}), 401

    user = next((user for user in users if user['email'] == auth.username), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Don't return the password hash
    user_data = {key: value for key, value in user.items() if key != 'password'}
    return jsonify(user_data)

