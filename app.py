from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load seed data from seedData.json file
with open('seedData.json', 'r') as f:
    seed_data = json.load(f)

# Route to add a new snippet
@app.route('/snippets', methods=['POST'])
def add_snippet():
    snippet_data = request.json
    # Assign an ID to the new snippet
    snippet_data['id'] = len(seed_data) + 1
    seed_data.append(snippet_data)
    # Write updated data back to the JSON file
    with open('seedData.json', 'w') as f:
        json.dump(seed_data, f, indent=2)
    return jsonify(snippet_data), 201

# Route to retrieve all snippets *** WITH BONUS ***
@app.route('/snippets', methods=['GET'])
def get_snippets():
    lang = request.args.get('lang')  # Get language parameter from the request
    print("Language:", lang)  # Debugging print statement
    if lang:
        # Filter snippets based on the language from search
        filtered_snippets = [snippet for snippet in seed_data if snippet.get('language', '').lower() == lang.lower()]
        print("Filtered snippets:", filtered_snippets)  # Debugging print statement
        return jsonify(filtered_snippets)
    else:
        # If no language param provided, return ALL
        return jsonify(seed_data)

# Route to retrieve a snippet by its ID
@app.route('/snippets/<int:id>', methods=['GET'])
def get_snippet_by_id(id):
    snippet = next((s for s in seed_data if s['id'] == id), None)
    if snippet:
        return jsonify(snippet)
    else:
        return jsonify({'error': 'Snippet not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
