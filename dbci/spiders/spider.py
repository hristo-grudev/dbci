import scrapy

from scrapy.loader import ItemLoader

from ..items import DbciItem
from itemloaders.processors import TakeFirst


class DbciSpider(scrapy.Spider):
	name = 'dbci'
	start_urls = ['http://www.db-ci.com/news.php?year=2020']

	def parse(self, response):
		post_links = response.xpath('//div[@class="main-column content-five"]//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="left-column"]//a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h2/text()').get()
		description = response.xpath('//div[@class="main-column content-five"]//text()[normalize-space() and not(ancestor::h2 | ancestor::em)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//em/text()').get()

		item = ItemLoader(item=DbciItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
