# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from pathlib import Path
import urllib
import requests

def get_website_list(filepath: str) -> list:
    """This method parses the document obtained '<from https://moz.com/top500>' into a list object that contains the urls. The .csv file must use the ',' character as separator.

    :param filepath: Path to the .csv file that contains the list.

    :return: A list of URLs, as strings.
    """
    clean_list = []
    
    if Path(filepath).exists():
        with open(filepath, 'r') as f:
            raw_list = f.readlines()

        raw_list.pop(0)
        for row in raw_list:
            field = row.split(',')[1].replace('\"', '')

            if field.startswith("http"):
                clean_list.append(field)
            elif field.startswith("www"):
                clean_list.append("https://" + field)
            else:
                clean_list.append("https://www." + field)

    return clean_list

class Page(scrapy.Item):
    url = scrapy.Field()
    page = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)

class MySpider(scrapy.Spider):
    name = "myspider"
    start_urls = get_website_list(Path(__file__).parent.absolute().resolve() / Path('top500Domains.csv'))

    def parse(self, response):
        return Page(url=response.url, page=response.text)

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    })

    process.crawl(MySpider)
    process.start() # the script will block here until the crawling is finished
