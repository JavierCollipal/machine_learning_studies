import scrapy
from ..models.content_config import ContentConfig
from ..extractors.humboldt_seed_extractor import HumboldtSeedExtractor
from ..parsers.humboldt_seed_parser import humboldt_seed_parse

class HumboldtSeedSpider(scrapy.Spider):
    name = 'humboldt_seed'

    def __init__(self, *args, **kwargs):
        start_urls = ['https://humboldtseedcompany.com/cannabis-deficiencies/']
        section_css = 'div.post-content'
        label_css = 'h2, h3'
        image_css = 'img'
        config = ContentConfig(
            stop_labels=['h2', 'h3'],
            text_xpath='.//text()'
        )
        self.extractor = HumboldtSeedExtractor(section_css, label_css, image_css, config)
        self.start_urls = start_urls
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        super(HumboldtSeedSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers={'User-Agent': self.user_agent}, meta={'spider': self})

    def parse(self, response):
        yield from humboldt_seed_parse(self, response)
