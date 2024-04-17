from flask import Flask, jsonify, request #importing necessary modules from Flask 
import json

app = Flask(__name__)

with open('seedData.json' , 'r') as f: #Open the seedData.json file in read mode 
    data = json.load(f) #Load JSON data from the file and store it in the data variable. 
    
@app.route('/snippets', methods=['GET', 'POST']) #Define route for /Snippets Endpoint with GET and POST methods
def snippets():
    if request.method == 'GET': #Checks if method request is GET
        return jsonify(data) #Return all data in JSON format if the req is GET
    elif request.method == 'POST': #Check if method request is POST
        new_snippet= request.json #Extract JSON data from the req 
        new_snippet['id'] = len(data) + 1 #Generate a unique ID for the new snippet
        data.append(new_snippet) #ADD new snippet to the data list
        with open('seedData.json', 'w') as f: #Open's file in write mode to update the data 
            json.dump(data, f, indent=2) #Write the update data back to the file 
        return jsonify(new_snippet), 201 #Return new snippet with HTTP status code 201 (created)
    
@app.route('/snippets/<int:id>', methods=['GET']) #Define a route /snippets/<id> endpoint with GET method 
def snippt_by_id(id):
    snippet = next((s for s in data if s['id'] == id), None) #Find the snippet with the ID
    if snippet: #If the snippet is found 
        return jsonify(snippet) # Return in JSON format
    else: #If snippet is not found 
        return jsonify({'error': "Snippet not found"}), 404 

if __name__ ==  '__main__':
    app.run(debug=True)