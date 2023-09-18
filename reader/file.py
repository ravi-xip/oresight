import logging

from bs4 import BeautifulSoup
from pyparsing import Optional

from llm.util import Utils


class File:
    def __init__(self):
        pass

    @staticmethod
    def read(path: str, normalize=False) -> str:
        """
        Given a path to a file, reads the contents and sends back the contents
        :param path: Path to the file
        :param normalize: Whether to normalize the contents or not
        :return:
        """
        contents = ""
        if path.endswith(".html"):
            try:
                contents = File.read_html(path)
            except Exception as e:
                logging.error(f"Error in reading HTML file: {e}")
                raise e
        if normalize:
            contents = Utils.normalize(contents)
        return contents

    @staticmethod
    def read_html(path: str) -> str:
        """
        Takes path to an HTML file, reads it and sends it back as a string
        :param path:
        :return:
        """
        # Step I: Check if the file is an HTML file
        if not path.endswith(".html"):
            raise Exception("File is not an HTML file")

        # Step II: Read the contents of the file
        with open(path, "r") as f:
            contents = f.read()
            # Clean up the contents so that only the text remains and send it back
            return File.clean_html(contents)

    @staticmethod
    def clean_html(content: str) -> str:
        """
        Cleans up the HTML content and sends back the text
        :param content:
        :return:
        """
        soup = BeautifulSoup(content, features="html.parser")
        return soup.get_text()
