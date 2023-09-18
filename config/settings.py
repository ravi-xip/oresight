# Configurations for the logger
import logging
import logging.config
import os
import json

# Load logging configuration from JSON file
path = os.path.dirname(os.path.abspath(__file__))
logging_config_file = os.path.join(path, 'logging_config.json')
with open(logging_config_file, 'r') as f:
    log_config = json.load(f)
    logging.config.dictConfig(log_config)

# Configurations for the app
OPENAI_CHAT_MODEL = "gpt-3.5-turbo-0613"
DEFAULT_TEMPERATURE = 0.0
DEFAULT_MAX_TOKENS = 500
SYSTEM_PROMPT = "You are an expert marketer who is helping find great prospects for a new product."
FALLBACK_ANSWER = "I'm sorry, I am not able to answer that question. Please try asking a different request."
