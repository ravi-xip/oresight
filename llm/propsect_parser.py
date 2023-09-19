import os
from typing import List, Dict

from entities.prospect import Prospect
from entities.website import Website
from llm.aiclient import AIClient
from reader.file import File


def parse_prospect(website_id: str, url: str, parse_json: dict) -> List[Prospect]:
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
        title = person.get('title')
        contact = person.get('contact')
        bio = person.get('bio')
        email = person.get('email')
        prospect_list.append(Prospect(name=name, email=email, bio=bio,
                                      phone=contact, url=url, website_id=website_id,
                                      interest=""))
    return prospect_list


class ProspectParser:
    """
    Given a document, extracts the prospects from it.
    """

    def __init__(self):
        self._aiclient = AIClient()

    def parse(self, website: Website, url_document_map: Dict[str, str]) -> List[Prospect]:
        prospect_list: List[Prospect] = []
        for url, document in url_document_map.items():
            prospect_list.extend(self.__parse_document(website, url, document))
        return prospect_list

    def __parse_document(self, website: Website, url: str, document: str) -> List[Prospect]:
        # Step I: Extract the entities from the document
        response_json = self._aiclient.extract_bio(document)

        # Step II: Translate the entities into prospects
        return parse_prospect(website.id, url, response_json)


if __name__ == '__main__':
    ai = AIClient()
    file = File()
    # Find the path to the base directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, 'data/test.html')
    if not os.path.exists(path):
        raise Exception(f'File {path} does not exist.')
    contents = file.read(path, normalize=True)
    prospects = parse_prospect('', 'www.google.com', ai.extract_bio(contents))
    for prospect in prospects:
        print(prospect.to_dict())
