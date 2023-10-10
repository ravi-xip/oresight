from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # noqa
from selenium.webdriver.support.ui import WebDriverWait

from crawler.utils.helper_methods import get_text_from_html


class OreSightDriver:
    def __init__(self):
        # self._setup_driver()
        self.links_list = []
        self._link_source_map = {}

    @property
    def link_source_map(self):
        return self._link_source_map

    def _setup_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.log_path = "chromedriver.log"
        self.driver = webdriver.Chrome(options=chrome_options)

    def _navigate_to_page(self, url):
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 5)
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "dummy-class")))
        except Exception as e:  # noqa
            pass

    def _get_links_from_page_source(
        self, url: str, page_source: str, filter_text: str
    ) -> list:
        soup = BeautifulSoup(page_source, "html.parser")

        self._link_source_map[url] = get_text_from_html(page_source)

        links = []
        for page_link in soup.find_all("a"):
            if filter_text in page_link.get("href", ""):
                links.append(page_link.get("href"))
        return links

    def _scroll_to_bottom_and_wait(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        wait = WebDriverWait(self.driver, 5)
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "dummy-class")))
        except Exception as e:  # noqa
            pass

    def crawl(self, url: str, max_links: int, filter_text: str) -> dict:
        self._navigate_to_page(url)
        iteration = 0
        while len(self.links_list) < max_links:
            iteration += 1
            self.links_list += self._get_links_from_page_source(
                f"{url}_{iteration}", self.driver.page_source, filter_text
            )

            # Deduplicate links in case there are repeats
            self.links_list = list(set(self.links_list))

            # Break if we've already reached max_links after deduplication
            if len(self.links_list) >= max_links:
                break

            self._scroll_to_bottom_and_wait()

        self.driver.quit()  # Close the driver when done
        return self._link_source_map


if __name__ == "__main__":
    ore_sight_driver = OreSightDriver()
    link_source_map = ore_sight_driver.crawl(
        url="https://www.reddit.com/r/BasketballTips/?rdt=53927",
        max_links=10,
        filter_text="comments",
    )
    for link, source in link_source_map.items():
        print(link, source)
