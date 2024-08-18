from flask import Flask, jsonify, render_template
import json
import os

app = Flask(__name__)

# File path to read the gamepad data
file_path = "gamepad_data.json"

@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/gamepad', methods=['GET'])
def gamepad():
    # Check if the file exists
    if not os.path.exists(file_path):
        return jsonify({"error": "No gamepad data available"}), 404

    # Read the gamepad data from the file
    with open(file_path, 'r') as f:
        gamepad_data = json.load(f)

    return jsonify(gamepad_data)

if __name__ == '__main__':
    app.run(debug=True)
