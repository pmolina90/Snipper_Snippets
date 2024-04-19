from flask import Flask, jsonify, request #importing necessary modules from Flask 
from encryption_utils. import encrypt_data, decrypt_data 
from authentication_utils import hash_password, verify_password
import json

app = Flask(__name__)

#loads the seed data 
with open('seedData.json' , 'r') as f: #Open the seedData.json file in read mode 
    data = json.load(f) #Load JSON data from the file and store it in the data variable. 
    
    # Dummy user data for testing
    users = [
        {'email': 'test@example.com', 'password': hash_password('password')}
]
    
@app.route('/snippets', methods=['GET', 'POST']) #Define route for /Snippets Endpoint with GET and POST methods
def snippets():
    if request.method == 'GET': #Checks if method request is GET
        decrypted_data = decrypt_data(data)#Decrpyt snippets before returning
        print("Decrypted data:", decrypted_data) #Prints decrypted data
        return jsonify(decrypt_data) #Return all data in JSON format if the req is GET
    elif request.method == 'POST': #Check if method request is POST
        new_snippet= request.json #Extract JSON data from the req 
        new_snippet['id'] = len(data) + 1 #Generate a unique ID for the new snippet
        encrypted_code = encrypt_data(new_snippet['code']) #Encrypt new data before saving
        print("Encrypted code:", encrypted_code) #Print encrypted code
        new_snippet['code'] = encrypted_code
        data.append(new_snippet) #ADD new snippet to the data list
        with open('seedData.json', 'w') as f: #Open's file in write mode to update the data 
            json.dump(data, f, indent=2) #Write the update data back to the file 
        return jsonify(new_snippet), 201 #Return new snippet with HTTP status code 201 (created)
    
@app.route('/snippets/<int:id>', methods=['GET']) #Define a route /snippets/<id> endpoint with GET method 
def snippt_by_id(id):
    snippet = next((s for s in data if s['id'] == id), None) #Find the snippet with the ID
    if snippet: #If the snippet is found 
        snippet['code'] = decrypt_data(snippet['code'])
        print("Decrypted snippet:", snippet) # Print decrypted snippet
        return jsonify(snippet) # Return in JSON format
    else: #If snippet is not found 
        return jsonify({'error': "Snippet not found"}), 404 

@app.route('/users', methods=['GET','POST'])
def users():
    if request.method == 'GET':  # Check if method request is GET
        email = request.headers.get('email')  # Extract email from request headers
        password = request.headers.get('password')  # Extract password from request headers
        if email and password:  # Check if email and password are provided
            user = next((u for u in users if u['email'] == email), None)  # Find user in users list based on email
            if user and verify_password(password, user['password']):  # Check if user exists and password is correct
                user_without_password = {k: v for k, v in user.items() if k != 'password'}  # Remove password from user data
                print("User:", user_without_password)  # Print user data without password
                return jsonify(user_without_password)  # Return user data without password
        return jsonify({'error': 'Unauthorized'}), 401  # Return unauthorized error if email or password is missing or incorrect

    elif request.method == 'POST':  # Check if method request is POST
        new_user_data = request.json  # Extract JSON data from the request
        hashed_password = hash_password(new_user_data['password'])  # Hash password before saving user
        new_user_data['password'] = hashed_password  # Update password with hashed value
        users.append(new_user_data)  # Add new user data to users list
        return jsonify({'message': 'User created successfully'}), 201  # Return success message with HTTP status code 201 (created)

if __name__ ==  '__main__':
    app.run(debug=True)