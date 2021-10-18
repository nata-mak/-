from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leroyparser import settings
from leroyparser.spiders.lmru import LmruSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    # query = input('')
    process.crawl(LmruSpider, query='новогодние украшения')

    process.start()