import json
import os
import random
import string
from logging.config import dictConfig
from multiprocessing import Process, Queue
from typing import List

import scrapy.crawler as crawler
from twisted.internet import reactor

from crawler.decover_spider import DecoverSpider
from crawler.utils.helper_methods import get_random_file_name

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://sys.stdout',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


def f(q, start_urls, allowed_domains, should_recurse, max_links, download_pdfs, file_name, url_filter):
    """
    :param start_urls: The initial set of urls to start the spider on
    :param allowed_domains: An extension of the filter, used to filter on allowed set of domains
    :param should_recurse: If we want the spider to dig in the website, this flag should be set to TRUE
    :param max_links: The maximum number of links after which the spider should be stopped
    :param download_pdfs: A flag to ensure whether PDFs from the website should be downloaded or not
    :param file_name: A temporary file in which the intermediate responses are stored
    :param url_filter: A substring filter that ensures only URLs that have the given substring are downloaded
    """
    try:
        runner = crawler.CrawlerRunner(
            settings={
                'ITEM_PIPELINES': {
                    'crawler.json_writer_pipeline.JsonWriterPipeline': 1,
                },
                'LOG_LEVEL': 'INFO',
                'USER_AGENT': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                              'Mobile/15E148',
                'REFERRER_POLICY': 'origin'
            }
        )
        deferred = runner.crawl(DecoverSpider,
                                start_urls=start_urls,
                                allowed_domains=allowed_domains,
                                should_recurse=should_recurse,
                                max_links=max_links,
                                download_pdfs=download_pdfs,
                                file_name=file_name,
                                filter=url_filter)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run(0)
        q.put(None)
    except Exception as e:
        q.put(e)


class WebSiteCrawlerScrapy:
    """
    This class is used to crawl a website using Scrapy.
    """

    def __init__(self):
        pass

    # The wrapper to make it run more times.
    def crawl(self,  # noqa
              start_urls: List[str],
              allowed_domains: List[str],
              should_recurse: bool,
              max_links: int,
              download_pdfs: bool,
              crawl_filter: str) -> dict:
        """
        Given a collection of start_urls, crawls and downloads the pages.

        :param start_urls: The initial set of urls to start the spider on
        :param allowed_domains: An extension of the filter, used to filter on allowed set of domains
        :param should_recurse: If we want the spider to dig in the website, this flag should be set to TRUE
        :param max_links: The maximum number of links after which the spider should be stopped
        :param download_pdfs: A flag to ensure whether PDFs from the website should be downloaded or not
        :param crawl_filter: A substring filter that ensures only URLs that have the given substring are downloaded

        For starters, here is an example:
        site = "https://law.justia.com/cases/federal/appellate-courts/ca7/"
        domain = "law.justia.com"  # noqa
        site_filter = "federal/appellate-courts/ca7"
        crawler = WebSiteCrawlerScrapy()
        site_results = crawler.crawl(
            start_urls=[site],
            allowed_domains=[domain],
            should_recurse=True,
            max_links=5,
            download_pdfs=False,
            crawl_filter=site_filter)
        print(site_results.keys())


        :return: A dictionary mapping url of the page downloaded to content of the page
        """
        # Preprocess the inputs. start_urls should begin with https
        for i in range(len(start_urls)):
            if not start_urls[i].startswith('https'):
                start_urls[i] = 'https://' + start_urls[i]
        feed_export_file_name = get_random_file_name()
        q = Queue()
        p = Process(target=f, args=(q, start_urls, allowed_domains, should_recurse, max_links,
                                    download_pdfs, feed_export_file_name, crawl_filter))
        p.start()
        result = q.get()
        p.join()

        # Read the results from the JSON file.
        results = {}

        # Step III: Go through and read the results from the JSON file.
        with open(feed_export_file_name, 'r') as file:
            for line in file:
                item = json.loads(line)
                for url, content in item.items():
                    results[url] = content

        # Step IV: Clean up (Delete the JSON file).
        if os.path.exists(feed_export_file_name):
            os.remove(feed_export_file_name)

        if result is not None:
            raise result
        return results


if __name__ == "__main__":
    site = "https://law.justia.com/cases/federal/appellate-courts/ca7/"
    domain = "law.justia.com"  # noqa
    site_filter = "federal/appellate-courts/ca7"
    crawler = WebSiteCrawlerScrapy()
    site_results = crawler.crawl(
        start_urls=[site],
        allowed_domains=[domain],
        should_recurse=True,
        max_links=2,
        download_pdfs=False,
        crawl_filter=site_filter)
    print(site_results.keys())
