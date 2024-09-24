import scrapy
from ..models.content_config import ContentConfig
from ..extractors.dutch_passion_extractor import DutchPassionExtractor
from ..parsers.dutch_passion_parser import dutch_passion_parse

class DutchPassionSpider(scrapy.Spider):
    name = 'dutch_passion'

    def __init__(self, *args, **kwargs):
        start_urls = ['https://dutch-passion.com/en/blog/a-visual-guide-to-cannabis-deficiencies-n987']
        section_css = 'div#blog-item-content'
        label_css = 'h3, h2'
        image_css = 'img'
        config = ContentConfig(
            stop_labels=['h2', 'h3'],
            text_xpath='.//text()'
        )
        self.extractor = DutchPassionExtractor(section_css, label_css, image_css, config)
        self.start_urls = start_urls
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        super(DutchPassionSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers={'User-Agent': self.user_agent}, meta={'spider': self})

    def parse(self, response):
        yield from dutch_passion_parse(self, response)
