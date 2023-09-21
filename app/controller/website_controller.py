import logging
import threading
from typing import List

from flask import Request

from app.database import get_db_session
from config.settings import DEFAULT_MAX_LINKS_TO_PARSE
from crawler.oresight_driver import OreSightDriver
from entities.prospect import Prospect
from entities.website import Website
from index.propsect_index import ProspectIndex
from llm.propsect_parser import ProspectParser
from repositories.prospect_repository import ProspectRepository
from repositories.website_repository import WebsiteRepository


def update_index_with_prospects(prospects: List[Prospect]):
    """
    Given a list of prospects, updates the index with the prospects.
    :param prospects:
    :return:
    """
    # Step I: Update the index with the prospects
    for prospect in prospects:
        ProspectIndex(meta={'id': prospect.id},
                      name=prospect.name,
                      bio=prospect.bio,
                      category=prospect.category,
                      url=prospect.url).save()


class WebsiteController:
    def __init__(self):
        self._crawler = OreSightDriver()
        self._session = get_db_session()
        self._website_repository = WebsiteRepository(self._session)
        self._prospect_repository = ProspectRepository(self._session)

    def prospect_by_id(self, prospect_id: str) -> Prospect:
        """
        Returns the prospect for a given prospect id.

        :param prospect_id: the id of the prospect.
        :return: the prospect.
        """
        try:
            return self._prospect_repository.find_by_id(prospect_id)
        except Exception as e:
            logging.error(f"Error while getting a prospect: {e}")
            raise "Error while getting a prospect"

    def all_prospects(self) -> list[Prospect]:
        """
        Returns all the prospects for a given website.

        :return: a list of prospects.
        """
        return self._prospect_repository.find_all()

    def all_prospects_for_website(self, website_id: str) -> list[Prospect]:
        """
        Returns all the prospects for a given website.

        :param website_id: the id of the website.
        :return: a list of prospects.
        """
        return self._prospect_repository.find_by_website_id(website_id)

    def all_websites(self) -> list[Website]:
        """
        Returns all the websites in the database.

        :return: a list of websites.
        """
        return self._website_repository.find_all()

    def index_website(self, request: Request) -> (str, int):
        """
        Triggers a background task for the website crawler to crawl a website and extract its content.

        :param request: the request object.
        :return: a tuple containing the message and the status code.
        """
        # Extract the parameters from the request
        request_json = request.get_json()
        if request_json is None:
            return "Missing parameters. name should not be empty.", 400

        # Extract name of the website from the request
        name = request_json.get('name') if request_json.get('name') else ''
        if name == '':
            return "Missing parameters. name should not be empty.", 400

        # Extract URL of the website from the request
        url = request_json.get('url') if request_json.get('url') else ''
        if url == '':
            return "Missing parameters. url should not be empty.", 400

        # Extract URL filter of the website from the request
        url_filter = request_json.get('url_filter') if request_json.get('url_filter') else ''

        max_links = request_json.get('max_links') if request_json.get('max_links') else DEFAULT_MAX_LINKS_TO_PARSE

        # Create an entry in the database for the website
        website = Website(name=name, url=url, url_filter=url_filter, max_links=max_links)
        try:
            website = self._website_repository.add(website)
            # Trigger this in a background thread
            threading.Thread(target=lambda: self.__crawl(website.id)).start()

            return "Website indexing in progress", 200

        except Exception as e:
            logging.error(f"Error while creating a website: {e}")
            return "Error while creating a website", 500

    def re_index_website(self, website_id: str) -> (str, int):
        """
        Given a website id, triggers a background task for the website crawler to crawl the website again and extract
        its content.

        :param website_id: The id of the website to be re-indexed
        :return: a tuple containing the message and the status code
        """
        pass

    def __crawl(self, website_id: str) -> List[Prospect]:
        """
        Given a website crawl request, triggers a background task for the website crawler to crawl the website and
        extract its content.
        :param website_id: The id of the website to be crawled
        :return: a list of prospects
        """

        # Step I: Extract the parameters from the request
        website = self._website_repository.find_by_id(website_id)

        # Step II: Trigger the crawler in a separate thread in the background
        url_content_dict = self._crawler.crawl(
            url=website.url,
            max_links=website.max_links,
            filter_text=website.url_filter)

        # Step III: Extract the results from the crawler
        logging.info(f"Finished crawling {website.url}")
        for url, content in url_content_dict.items():
            logging.debug(f"URL: {url}")
            logging.debug(f"Content: {content}")

        # Step IV: Parse the results to extract all the prospects
        prospect_parser = ProspectParser()
        prospect_list = prospect_parser.parse(url_content_dict)

        # Step V: Save the prospects to the database
        prospects_added = []
        for prospect in prospect_list:
            try:
                self._prospect_repository.add(prospect)
                prospects_added.append(prospect)
            except Exception as e:
                logging.error(f"Error while adding a prospect: {e}")

        logging.info(f"Finished parsing {website.url} and added {len(prospects_added)} prospects")

        # Step VI: Update the website status
        self.__update_website_status(website_id, status="INDEXING", num_prospects=len(prospects_added))

        # Step VII: Update the index with the prospects
        update_index_with_prospects(prospects_added)

        # Step VIII: Update the website status
        self.__update_website_status(website_id, status="COMPLETED")

        # If debugging is enabled, print the prospects added
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug(f"Here are the prospects added:\n")
            for prospect in prospects_added:
                logging.debug(prospect.to_dict())
            logging.debug(f"Finished printing the prospects added")

        return prospects_added

    def __update_website_status(self, website_id: str, status: str, num_prospects: int = -1) -> Website:
        """

        :param website_id:
        :param status:
        :param num_prospects:
        :return:
        """
        website = self._website_repository.find_by_id(website_id)
        if not website:
            raise ValueError(f"Website with id {website_id} does not exist")

        if status in ['PROCESSING', 'INDEXING', 'COMPLETED', 'FAILED']:
            website.status = status

        if num_prospects >= 0:
            website.num_prospects = num_prospects

        website = self._website_repository.update(website)
        logging.debug(f"Updated website: {website.to_dict()}")
        return website
