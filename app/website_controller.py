class WebsiteController:
    def __init__(self):
        self._crawler = None

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

        if self._crawler is not None:
            self._crawler.crawl()
        return "Website indexed successfully", 200

    def re_index_website(self, website_id: str) -> (str, int):
        """
        Given a website id, triggers a background task for the website crawler to crawl the website again and extract
        its content.

        :param website_id:
        :return:
        """
        pass
