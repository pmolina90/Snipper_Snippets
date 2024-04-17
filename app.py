from flask import Flask, jsonify
import json

app = Flask(__name__)

with open('seedData.json' , 'r') as f:
    data = json.load(f)
    
@app.route('/snippets')
def get_snippets():
    return jsonify(data)

if __name__ ==  '__main__':
    app.run(debug=True)