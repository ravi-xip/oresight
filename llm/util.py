import re


class Utils:

    @staticmethod
    def normalize(text: str) -> str:
        return re.sub(r'[^a-zA-Z0-9 .:_/]', '', text)
