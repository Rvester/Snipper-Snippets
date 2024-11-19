from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load seed data from seedData.json
with open('seedData.json', 'r') as file:
    snippets = json.load(file)

# Endpoint to get all snippets
@app.route('/snippets', methods=['GET'])
def get_snippets():
    lang = request.args.get('language')
    if lang:
        filtered_snippets = [s for s in snippets if s['language'].lower() == lang.lower()]
        return jsonify(filtered_snippets), 200
    return jsonify(snippets), 200

# Endpoint to get a snippet by ID
@app.route('/snippets/<int:id>', methods=['GET'])
def get_snippet_by_id(id):
    snippet = next((s for s in snippets if s['id'] == id), None)
    if snippet:
        return jsonify(snippet), 200
    return jsonify({"error": "Snippet not found"}), 404

# Endpoint to create a new snippet
@app.route('/snippets', methods=['POST'])
def create_snippet():
    data = request.json
    if not data or 'language' not in data or 'code' not in data:
        return jsonify({"error": "Invalid data"}), 400
    new_id = max(snippet['id'] for snippet in snippets) + 1 if snippets else 1
    new_snippet = {
        "id": new_id,
        "language": data['language'],
        "code": data['code']
    }
    snippets.append(new_snippet)
    return jsonify(new_snippet), 201

if __name__ == '__main__':
    app.run(debug=True)
