import threading

from sqlalchemy.testing.plugin.plugin_base import logging

from crawler.website_crawler_scrapy import WebSiteCrawlerScrapy


class WebsiteController:
    def __init__(self):
        self._crawler = WebSiteCrawlerScrapy()

    def index_website(self, request) -> (str, int):
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

        self.__crawl(request)

        return "Website indexed successfully", 200

    def re_index_website(self, website_id: str) -> (str, int):
        """
        Given a website id, triggers a background task for the website crawler to crawl the website again and extract
        its content.

        :param website_id:
        :return:
        """
        pass

    def __crawl(self, request):
        """
        Given a website crawl request, triggers a background task for the website crawler to crawl the website and
        extract its content.
        
        :param request:
        :return:
        """

        # Step I: Extract the parameters from the request
        request_json = request.get_json()
        name = request_json.get('name') if request_json.get('name') else ''
        url = request_json.get('url') if request_json.get('url') else ''
        crawl_filter = request_json.get('filter') if request_json.get('filter') else ''
        if url.startswith('http://') or url.startswith('https://'):
            domain = url.split('/')[2]
        else:
            raise Exception(f"Invalid URL: {url}")
        start_urls = [url]
        allowed_domains = [domain]
        should_recurse = True
        max_links = 10
        download_pdfs = False
        crawl_filter = crawl_filter

        # Step II: Trigger the crawler
        crawl_thread = threading.Thread(target=lambda: setattr(crawl_thread, 'response',
                                                               self._crawler.crawl(
                                                                   start_urls, allowed_domains,
                                                                   should_recurse, max_links,
                                                                   download_pdfs, crawl_filter)))
        crawl_thread.start()
        crawl_thread.join()

        # Step III: Extract the results from the crawler
        url_content_dict = getattr(crawl_thread, 'response')
        logging.info(f"Finished crawling {url}")
        for url, content in url_content_dict.items():
            logging.info(f"URL: {url}")
            logging.info(f"Content: {content}")
