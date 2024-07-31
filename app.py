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


## POST method with excel file and results will be in json (not excel)

# from flask import Flask, request, jsonify
# import pandas as pd
# from werkzeug.utils import secure_filename
# import os
# import logging

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = '/tmp'

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# # Define required columns
# REQUIRED_COLUMNS = ['Test1', 'Test2']

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     try:
#         if 'file' not in request.files:
#             app.logger.error('No file part in the request')
#             return jsonify({'error': 'No file part in the request'}), 400

#         file = request.files['file']

#         if file.filename == '':
#             app.logger.error('No selected file')
#             return jsonify({'error': 'No selected file'}), 400

#         filename = secure_filename(file.filename)
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)

#         # Log file details
#         app.logger.info(f'File {filename} saved to {file_path}')
        
#         # Process the file
#         df = pd.read_excel(file_path)

#         # Check for required columns
#         missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
#         if missing_columns:
#             app.logger.error(f'Missing columns: {", ".join(missing_columns)}')
#             return jsonify({'error': f'Required columns not found: {", ".join(missing_columns)}'}), 400

#         # Ensure correct data types
#         if 'Test1' in df.columns:
#             df['Test1'] = df['Test1'].astype(str)  # Convert to string
#         if 'Test2' in df.columns:
#             df['Test2'] = pd.to_numeric(df['Test2'], errors='coerce')  # Convert to numeric, coercing errors to NaN

#         # Example data transformation
#         df['NewCol1'] = df['Test1'] + '_transformed'
#         df['NewCol2'] = df['Test2'] * 2
#         df['NewCol3'] = df['Test1'] + '_' + df['Test2'].astype(str)

#         result = df.to_json(orient='records')
#         return jsonify({'status': 'success', 'transformed_data': result}), 200

#     except Exception as e:
#         app.logger.error(f'Error: {str(e)}')
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)

###Send back the excel

from flask import Flask, request, jsonify, send_file
import pandas as pd
from io import BytesIO

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        df = pd.read_excel(file)

        # Ensure columns are converted to appropriate types
        df['Test1'] = pd.to_numeric(df['Test1'], errors='coerce')  # Convert to numeric, coerce errors
        df['Test2'] = pd.to_numeric(df['Test2'], errors='coerce')  # Convert to numeric, coerce errors

        # Process the DataFrame and add new columns
        df['NewCol1'] = df['Test1'].astype(str) + '_transformed'
        df['NewCol2'] = df['Test2'] * 2
        df['NewCol3'] = df['Test1'].astype(str) + '_' + df['Test2'].astype(str)

        # Create an in-memory Excel file
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='TransformedData')
        output.seek(0)

        return send_file(
            output,
            as_attachment=True,
            download_name='transformed_data.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

