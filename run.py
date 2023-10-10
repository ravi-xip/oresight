import logging
import time
import os

from elasticsearch_dsl import connections
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy.session import Session

from app.controller.chat_handler import ChatController
from app.controller.website_controller import WebsiteController
from app.database import db, Session
from config.settings import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from index.propsect_index import ProspectIndex
from middlewares.remove_prefix_middleware import RemovePrefixMiddleware

from elasticsearch_dsl.connections import connections
from elasticsearch.exceptions import ConnectionError


def create_app():
    """
    Sets up the Flask app.
    :return: a handle to the Flask app.
    """
    app = Flask(__name__)
    app.config["CORS_HEADERS"] = "Content-Type"
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
    db.init_app(app)
    CORS(
        app,
        resources={
            r"/*": {"origins": ["http://localhost:3000", "https://ravi-xip.ngrok.io"]}
        },
    )
    app.wsgi_app = RemovePrefixMiddleware(app.wsgi_app)
    return app


def connect_to_es(max_retries=5, base_delay=2):
    """
    Initialize the Elasticsearch connection and create the index.
    Uses retries with exponential backoff in case of connection issues.
    """
    retries = 0

    while retries < max_retries:
        try:
            es_host = os.environ.get("ES_HOST", "elasticsearch")
            es_port = os.environ.get("ES_PORT", "9200")
            connections.create_connection(hosts=[f"http://{es_host}:{es_port}"])
            ProspectIndex.init()
            return  # Connection successful
        except ConnectionError:
            wait_time = base_delay * (2**retries)
            print(f"Failed to connect to Elasticsearch. Retrying in {wait_time}s...")
            time.sleep(wait_time)
            retries += 1

    print(f"Failed to connect to Elasticsearch after {max_retries} attempts.")


def start_flask_server():
    """
    Starts the Flask server.
    """
    app = create_app()
    with app.app_context():
        # Initialize the database.
        Session.configure(bind=db.engine, autoflush=False)
        db.create_all()
        db.session.commit()

        # Initialize the controller.
        website_controller = WebsiteController()
        chat_controller = ChatController()

        connect_to_es()

    # Create a route for the root of the app
    @app.route("/", methods=["GET"])
    def ping():
        return "Oresight-Ok", 200

    @app.route("/health", methods=["GET"])
    def health_check():
        return "Oresight-Ok-Health", 200

    @app.route("/api/v1/chat", methods=["GET"])
    def chat():
        # Parse the request args and get the query.
        query = request.args.get("query")
        conversation = request.args.get("conversation")
        if query is None:
            return jsonify({"message": "Query not found"}), 400
        response = chat_controller.chat(query, conversation)
        return jsonify({"text": response}), 200

    @app.route("/api/v1/stream/chat", methods=["GET"])
    def stream_chat():
        return "Oresight-Ok", 200

    @app.route("/api/v1/prospects", methods=["GET"])
    def all_prospects():
        prospects = website_controller.all_prospects()
        prospects = [prospect.to_dict() for prospect in prospects]
        return jsonify(prospects), 200

    @app.route("/api/v1/prospects/website/<website_id>", methods=["GET"])
    def all_prospects_for_website(website_id):
        prospects = website_controller.all_prospects_for_website(website_id)
        return jsonify(prospects), 200

    @app.route("/api/v1/prospects/<prospect_id>", methods=["GET"])
    def prospect_by_id(prospect_id):
        prospects = website_controller.prospect_by_id(prospect_id)
        return jsonify(prospects), 200

    @app.route("/api/v1/websites", methods=["GET"])
    def all_websites():
        websites = website_controller.all_websites()
        # Convert the list of websites to a list of dictionaries.
        websites = [website.to_dict() for website in websites]
        return jsonify(websites), 200

    @app.route("/api/v1/websites", methods=["POST"])
    @app.route("/api/v1/website", methods=["POST"])
    def index_website():
        msg, status = website_controller.index_website(request)
        return jsonify({"message": msg}), status

    @app.route("/api/v1/website/<website_id>", methods=["POST"])
    def re_index_website(website_id):
        msg, status = website_controller.re_index_website(website_id)
        return jsonify({"message": msg}), status

    # Start the Flask app.
    app.run(host="0.0.0.0", port=8080, debug=False)


if __name__ == "__main__":
    logging.info(f"Starting the flask server")
    start_flask_server()
