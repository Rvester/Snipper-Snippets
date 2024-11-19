import json
from flask import Flask
from routes import snippet_routes, user_routes
from models import snippets, users

app = Flask(__name__)

# Load seed data from the file
def load_seed_data():
    with open('seedData.json', 'r') as file:
        data = json.load(file)
        snippets.extend(data["snippets"])  # Add seed snippets to the snippets list
        users.extend(data["users"])        # Add seed users to the users list

# Initialize data
load_seed_data()

# Register routes
app.register_blueprint(snippet_routes)
app.register_blueprint(user_routes)

if __name__ == '__main__':
    app.run(debug=True)
