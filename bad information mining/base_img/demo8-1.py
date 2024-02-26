import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
import time
import random

class ImageScraper:
    def __init__(self, url):
        self.url = url
        url_info = urlparse(url)
        self.base_url = url_info.scheme + "://" + url_info.netloc
        self.page_links = set()

    def open_url(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
            "Referer": "https://www.douban.com"
        }
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.content
        else:
            print(res.text)

    def store_page_links(self):
        content = self.open_url(self.url)
        soup = BeautifulSoup(content, "html.parser")
        page_tags = soup.find("div", attrs={"id": "pages"}).find_all("a")
        for page_tag in page_tags:
            self.page_links.add(page_tag['href'])

    def download_images(self, page_link):
        page_content = self.open_url(self.base_url + page_link)
        soup = BeautifulSoup(page_content, "html.parser")
        img_tags = soup.find("div", class_="content").find("center").find_all("img")
        if len(self.page_links) == 0:
            return
        for img_tag in img_tags:
            img_src = img_tag["src"]
            img_content = self.open_url(img_src)
            fn = str(int(time.time())) + str(random.randint(100, 999)) + ".jpg"
            with open(fn, "wb") as f:
                f.write(img_content)

    def run(self):
        self.store_page_links()
        if not os.path.isdir("imgs"):
            os.mkdir("imgs")
        os.chdir("imgs")
        for page_link in self.page_links:
            self.download_images(page_link)

url_to_scrape = "[^1^][1]"
scraper = ImageScraper(url_to_scrape)
scraper.run()
