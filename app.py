# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/', methods=['POST'])
def submit():
    # Get the JSON data from the request
    data = request.get_json()
    
    # Process the data as needed
    # For example, you could print it or perform some operations
    print(data)
    
    # Return a response
    return jsonify({'status': 'success', 'data_received': data}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

