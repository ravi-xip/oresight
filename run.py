# This is a sample Python script.

from llm.aiclient import AIClient
from reader.file import File
import logging


def extract_bio_example(file_path: str):
    """
    This is an example of how to use the AI Client to extract a bio from a file.
    :param file_path:
    :return:
    """
    contents = File.read(file_path, True)
    client = AIClient()
    response = client.extract_bio(contents)
    logging.info(f"Response: {response}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    extract_bio_example(file_path="data/test.html")
