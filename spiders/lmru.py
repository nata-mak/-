#1) Взять любую категорию товаров на сайте Леруа Мерлен. Собрать следующие данные:
# ● название;
# ● все фото;
# ● ссылка;
# ● цена.
#
# Реализуйте очистку и преобразование данных с помощью ItemLoader. Цены должны быть в виде числового значения.

import scrapy
from scrapy.http import HtmlResponse
from leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader

class LmruSpider(scrapy.Spider):
    name = 'lmru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query):
        super().__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={query}']

    def parse(self, response):
        next_page = response.xpath("//a[contains(@aria-label, 'Следующая страница')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//div[@data-qa-product]/a")
        for link in links:
            yield response.follow(link, callback=self.parse_leroy)

    def parse_leroy(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_value('link', response.url)
        loader.add_xpath('title', "//h1/text()")
        loader.add_xpath('price', "//span[@slot = 'price']/text()")
        loader.add_xpath('currency', "//span[@slot = 'currency']/text()")
        loader.add_xpath('photos', "//picture[@slot = 'pictures']/img/@src")
        yield loader.load_item()
