import scrapy
from scrapy_splash import SplashRequest
from config.constance import EIGEN_TX_URL


class EigentxSpider(scrapy.Spider):
    name = "eigentx"

    custom_settings = {
        "SPLASH_URL": "http://localhost:8050",
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy_splash.SplashCookiesMiddleware": 723,
            "scrapy_splash.SplashMiddleware": 725,
            "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 810,
        },
        "SPIDER_MIDDLEWARES": {
            "scrapy_splash.SplashDeduplicateArgsMiddleware": 100,
        },
        "DUPEFILTER_CLASS": "scrapy_splash.SplashAwareDupeFilter",
    }

    def __init__(self, txs):
        self.txs = txs

    def start_requests(self):
        urls = [EIGEN_TX_URL + tx for tx in self.txs]
        for url in urls:
            yield SplashRequest(
                url,
                self.parse,
                args={"wait": 0.5, "timeout": 30},
            )

    def parse(self, response):
        print("")
        print("response:")
        print(response.css("div").getall())
        print("")
