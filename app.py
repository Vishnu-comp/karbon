from flask import Flask, request, jsonify
import json
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS  # Import CORS
from model import probe_model_5l_profit  # Your model logic from Module 1

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = {'json'}

# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET'])
def index():
    return "Welcome to the Flask API. Please use the '/upload' endpoint to upload data."

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Process the file using the model
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Get the results from model.py
        try:
            result = probe_model_5l_profit(data["data"])
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500  # Handle model errors

    return jsonify({"error": "File type not allowed"}), 400

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
