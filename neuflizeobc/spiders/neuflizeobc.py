import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from neuflizeobc.items import Article


class NeuflizeobcSpider(scrapy.Spider):
    name = 'neuflizeobc'
    start_urls = ['https://www.neuflizeobc.fr/fr/actualites/tous-les-articles.html']

    def parse(self, response):
        links = response.xpath('//section[@data-component-type="news-article-overview"]//a[@class="btn-link"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//div[@class="date"]/text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@class="px-2 px-md-5 px-lg-0 pt-3 pt-md-4 "]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
