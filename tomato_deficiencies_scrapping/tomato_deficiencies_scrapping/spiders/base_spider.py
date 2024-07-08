import scrapy
from ..models.content_config import ContentConfig
from ..models.extractor import Extractor

class BaseContentSpider(scrapy.Spider):
    name = 'base_content_spider'

    def __init__(self, start_urls, section_css, label_css, image_css, config, user_agent, parse_function, *args, **kwargs):
        super(BaseContentSpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls
        self.extractor = Extractor(section_css, label_css, image_css, config)
        self.user_agent = user_agent
        self.parse_function = parse_function

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers={'User-Agent': self.user_agent}, meta={'spider': self})

    def parse(self, response):
        return self.parse_function(self, response)
