import scrapy
from scrapy.crawler import CrawlerProcess

from collector.eigenphi.EigentxSpider import EigentxSpider


def crawl_eigentx(txs):
    process = CrawlerProcess()

    process.crawl(EigentxSpider, txs)
    process.start()  # the script will block here until the crawling is finished
