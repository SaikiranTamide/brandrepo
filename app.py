## Get Method


# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)


## POST Method - with no file

# from flask import Flask, request, jsonify

# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

# @app.route('/', methods=['POST'])
# def submit():
#     # Get the JSON data from the request
#     data = request.get_json()
    
#     # Process the data as needed
#     # For example, you could print it or perform some operations
#     print(data)
    
#     # Return a response
#     return jsonify({'status': 'success', 'data_received': data}), 200

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)


## POST method with excel file

from flask import Flask, request, jsonify
import pandas as pd
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp'  # Temporary folder for uploaded files

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Read the Excel file
    df = pd.read_excel(file_path)

    # Check if the required columns exist
    if 'Test1' not in df.columns or 'Test2' not in df.columns:
        return jsonify({'error': 'Required columns not found'}), 400
    
    # Perform the transformation
    df['NewCol1'] = df['Test1'] + '_transformed'  # Example transformation
    df['NewCol2'] = df['Test2'] * 2  # Example transformation
    df['NewCol3'] = df['Test1'] + '_' + df['Test2'].astype(str)  # Example transformation

    # You can add more transformations as needed

    # Convert DataFrame to JSON and return it
    result = df.to_json(orient='records')

    return jsonify({'status': 'success', 'transformed_data': result}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

