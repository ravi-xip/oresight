import logging

from flask import Flask
from flask_cors import CORS

from app.database import db
from config.settings import SQLALCHEMY_DATABASE_URI


def create_app():
    """
    Sets up the Flask app.
    :return: a handle to the Flask app.
    """
    app = Flask(__name__)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}})
    return app


def start_flask_server():
    """
    Starts the Flask server.
    """
    app = create_app()
    with app.app_context():
        db.create_all()

    @app.route('/', methods=['GET'])
    def ping():
        return "OreSight-Ok", 200

    # Create a route for the root of the app
    @app.route('/health', methods=['GET'])
    def health_check():
        return "Callosum-Ok", 200

    # Start the Flask app.
    app.run(host='0.0.0.0', port=80, debug=True)


if __name__ == '__main__':
    logging.info(f'Starting the flask server')
    start_flask_server()
