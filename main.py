# This is a sample Python script.

from llm.aiclient import AIClient
from reader.file import File
import logging

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file_path = "data/test.html"
    contents = File.read(file_path, True)
    print(contents)
    client = AIClient()
    response = client.extract_bio(contents)
    logging.info(f"Response: {response}")
