# Configurations for the logger
import json
import logging.config
import os

# Load logging configuration from JSON file
path = os.path.dirname(os.path.abspath(__file__))
logging_config_file = os.path.join(path, "logging_config.json")
with open(logging_config_file, "r") as f:
    log_config = json.load(f)
    logging.config.dictConfig(log_config)

# Configurations for the app
OPENAI_CHAT_MODEL = "gpt-3.5-turbo-16k"
OPENAI_CHAT_MODEL_LARGE = "gpt-4"
DEFAULT_TEMPERATURE = 0.0
DEFAULT_MAX_TOKENS = 2000
DEFAULT_MAX_LINKS_TO_PARSE = 50
SYSTEM_PROMPT = (
    "You are an expert marketer who is helping find great prospects for a new product."
)
FALLBACK_ANSWER = "I'm sorry, I am not able to answer that question. Please try asking a different request."
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = "text-embedding-ada-002"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configurations for the database
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "SQLALCHEMY_DATABASE_URI", "postgresql://localhost:5432/postgres"
)
