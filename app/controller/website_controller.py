import threading
from typing import List

from flask import Request
from sqlalchemy.testing.plugin.plugin_base import logging

from app.database import get_db_session
from config.settings import DEFAULT_MAX_LINKS_TO_PARSE
from crawler.website_crawler_scrapy import WebSiteCrawlerScrapy
from entities.prospect import Prospect
from entities.website import Website
from llm.propsect_parser import ProspectParser
from repositories.prospect_repository import ProspectRepository
from repositories.website_repository import WebsiteRepository


class WebsiteController:
    def __init__(self):
        self._crawler = WebSiteCrawlerScrapy()
        self._session = get_db_session()
        self._website_repository = WebsiteRepository(self._session)
        self._prospect_repository = ProspectRepository(self._session)

    def index_website(self, request: Request) -> (str, int):
        """
        Triggers a background task for the website crawler to crawl a website and extract its content.

        :param request: the request object.
        :return: a tuple containing the message and the status code.
        """

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

        # Create an entry in the database for the website
        website = Website(name=name, url=url)
        try:
            website = self._website_repository.add(website)
            self.__crawl(request, website)
            return "Website indexed successfully", 200

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

    def __crawl(self, request: Request, website: Website) -> List[Prospect]:
        """
        Given a website crawl request, triggers a background task for the website crawler to crawl the website and
        extract its content.

        :param request: The request object containing the parameters for the website crawl request
        :param website: The website from which the prospects are to be extracted
        :return:
        """

        # Step I: Extract the parameters from the request
        request_json = request.get_json()
        url = request_json.get('url') if request_json.get('url') else ''
        crawl_filter = request_json.get('filter') if request_json.get('filter') else ''
        if url.startswith('http://') or url.startswith('https://'):
            domain = url.split('/')[2]
        else:
            raise Exception(f"Invalid URL: {url}")
        start_urls = [url]
        allowed_domains = [domain]
        max_links = DEFAULT_MAX_LINKS_TO_PARSE
        should_recurse = True
        download_pdfs = False

        # Step II: Trigger the crawler
        crawl_thread = threading.Thread(target=lambda: setattr(crawl_thread, 'response',
                                                               self._crawler.crawl(
                                                                   start_urls=start_urls,
                                                                   allowed_domains=allowed_domains,
                                                                   should_recurse=should_recurse,
                                                                   max_links=max_links,
                                                                   download_pdfs=download_pdfs,
                                                                   crawl_filter=crawl_filter)))
        crawl_thread.start()
        crawl_thread.join()

        # Step III: Extract the results from the crawler
        url_content_dict = getattr(crawl_thread, 'response')
        logging.info(f"Finished crawling {url}")
        for url, content in url_content_dict.items():
            logging.info(f"URL: {url}")
            logging.info(f"Content: {content}")

        # Step IV: Parse the results to extract all the prospects
        prospect_parser = ProspectParser()
        prospect_list = prospect_parser.parse(website, url_content_dict)

        # Step V: Save the prospects to the database
        prospects_added = []
        for prospect in prospect_list:
            try:
                self._prospect_repository.add(prospect)
                prospects_added.append(prospect)
            except Exception as e:
                logging.error(f"Error while adding a prospect: {e}")

        logging.info(f"Finished parsing {url} and added {len(prospects_added)} prospects")

        # If debugging is enabled, print the prospects added
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug(f"Here are the prospects added:\n")
            for prospect in prospects_added:
                logging.debug(prospect.to_dict())
            logging.debug(f"Finished printing the prospects added")

        return prospects_added
