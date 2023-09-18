from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}})


@app.route('/')
def ping():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    # Step I: Run the application.
    app.run(host='0.0.0.0', port=80, debug=True)
