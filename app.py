from flask import Flask, jsonify, request
import json
from encryption_utils import read_symmetric_key, encrypt_data, decrypt_data

app = Flask(__name__)

# Load seed data
with open('seedData.json', 'r') as f:
    seed_data = json.load(f)

# Read symmetric encryption key from file
symmetric_key = read_symmetric_key('./symmetric_key.txt')

@app.route('/snippets', methods=['POST'])
def add_snippet():
    snippet_data = request.json
    print("Original code:", snippet_data['code'])  # Print original code
    # Encrypt the code content before saving
    encrypted_code = encrypt_data(snippet_data['code'], symmetric_key)
    print("Encrypted code:", encrypted_code)  # Print encrypted code
    snippet_data['code'] = encrypted_code
    # Assign an ID to the new snippet
    snippet_data['id'] = len(seed_data) + 1
    seed_data.append(snippet_data)
    # Write updated data back to the JSON file
    with open('seedData.json', 'w') as f:
        json.dump(seed_data, f, indent=2)
    return jsonify(snippet_data), 201

@app.route('/snippets', methods=['GET'])
def get_snippets():
    # Decrypt the code content before returning
    decrypted_data = [{**snippet, 'code': decrypt_data(snippet['code'], symmetric_key)} for snippet in seed_data]
    print("Decrypted data:", decrypted_data)  # Print decrypted data
    return jsonify(decrypted_data)

if __name__ == '__main__':
    app.run(debug=True)
