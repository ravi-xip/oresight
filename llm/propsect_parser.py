import os
from typing import List, Dict

from entities.prospect import Prospect
from llm.aiclient import AIClient
from reader.file import File


def parse_prospect(base_url: str, parse_json: dict) -> List[Prospect]:
    """
    {'people': [{'name': 'John J. Gilluly III', 'title': 'Partner',
    'bio': 'John Gilluly represents clients across a range of industries and focuses on capital markets transactions,
    SEC reporting and compliance, mergers and acquisitions, private equity and venture capital transactions,
    and corporate governance matters.', 'contact': '1 512 457 7090', 'email': 'john.gillulydlapiper.com'}]}

    :return:
    """
    people = parse_json.get('people')
    if not people:
        return []
    prospect_list: List[Prospect] = []
    for person in people:
        name = person.get('name')
        category = person.get('category')
        bio = person.get('bio')
        bio_url = base_url + '/' + name
        prospect_list.append(Prospect(name=name, bio=bio, category=category, url=bio_url))
    return prospect_list


class ProspectParser:
    """
    Given a document, extracts the prospects from it.
    """

    def __init__(self):
        self._ai_client = AIClient()

    def parse(self, url_document_map: Dict[str, str]) -> List[Prospect]:
        prospect_list: List[Prospect] = []
        for url, document in url_document_map.items():
            try:
                prospect_list.extend(self.__parse_document(document))
            except Exception as e:
                continue
        return prospect_list

    def __parse_document(self, document: str) -> List[Prospect]:
        # Step I: Extract the entities from the document
        response_json = self._ai_client.extract_info(document)

        # Step II: Translate the bio url
        base_url = f"https://www.reddit.com"

        # Step II: Translate the entities into prospects
        return parse_prospect(base_url, response_json)


if __name__ == '__main__':
    ai = AIClient()
    file = File()
    # Find the path to the base directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, 'data/crawl.txt')
    if not os.path.exists(path):
        raise Exception(f'File {path} does not exist.')
    contents = file.read(path, normalize=True)
    info = ai.extract_info(contents)

    for key, value in info.items():
        print(key, value)
