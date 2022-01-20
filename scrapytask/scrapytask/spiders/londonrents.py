import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from ..property import Property


class LondonrelocationSpider(scrapy.Spider):
    name = 'londonrelocation'
    allowed_domains = ['londonrelocation.com']
    start_urls = ['https://londonrelocation.com/properties-to-rent/']

    def parse(self, response):
        links = response.xpath('//div[@class="wd-25 pd-8"]/a//@href').getall()

        for link in range(4):
            yield Request(url=links[link],
                          callback=self.parse_area)

    def parse_area(self, response):
        area_urls = response.xpath('//div[@class="h4-space"]//a//@href').getall()
        for area_url in area_urls:
            yield Request(url=f"https://londonrelocation.com{area_url}",
                          callback=self.parse_area_pages)

        next_pages = response.xpath('//div[@class="pagination"]//li[last()]//@href').get()
        if next_pages is not None:
            yield Request(url=next_pages,
                          callback=self.parse_area)



    def parse_area_pages(self, response):
        title = response.xpath('//h2//text()').getall()[:2]
        price = response.xpath('//h3//text()').get().replace("pw","").replace("pcm",'').strip().replace("£",'')

        property = ItemLoader(item=Property())
        property.add_value('title', title)
        property.add_value('price', int(price))
        property.add_value('url', response.url)
        return property.load_item()
