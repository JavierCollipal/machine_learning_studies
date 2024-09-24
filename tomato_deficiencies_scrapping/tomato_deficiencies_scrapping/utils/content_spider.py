import scrapy

class ContentConfig:
    def __init__(self, stop_labels, text_xpath):
        self.stop_labels = stop_labels
        self.text_xpath = text_xpath

class Extractor:
    def __init__(self, section_css, label_css, image_css, config):
        self.section_css = section_css
        self.label_css = label_css
        self.image_css = image_css
        self.config = config

    def extract_label(self, element):
        label_element = element.css('::text').get()
        if label_element:
            return label_element.strip()
        return None

    def extract_content(self, label_element, response):
        content = []
        next_elements = label_element.xpath('./following-sibling::*')
        for element in next_elements:
            if element.xpath('name()').get() in self.config.stop_labels:
                break
            images = self.extract_images(element, response)
            texts = element.xpath(self.config.text_xpath).extract()
            if images or texts:
                content.append({
                    'images': images,
                    'text': ' '.join(text.strip() for text in texts if text.strip())
                })
        return content if content else None

    def extract_images(self, element, response):
        images = []
        img_elements = element.css(self.image_css)
        for img in img_elements:
            img_src = img.css('::attr(src)').get()
            if img_src:
                caption = self.extract_caption(img)
                images.append({'image_url': response.urljoin(img_src), 'caption': caption})
        return images if images else None

    def extract_caption(self, img):
        caption_element = img.xpath('./following-sibling::p[1]//text()').get()
        if caption_element:
            return caption_element.strip()
        return None

class ContentSpider(scrapy.Spider):
    name = 'content_spider'

    def __init__(self, start_urls, section_css, label_css, image_css, config, *args, **kwargs):
        super(ContentSpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls
        self.extractor = Extractor(section_css, label_css, image_css, config)
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers={'User-Agent': self.user_agent}, meta={'spider': self})

    def parse(self, response):
        section = self.extract_section(response)
        if section:
            self.parse_section(section, response)

    def extract_section(self, response):
        section = response.css(self.extractor.section_css)
        self.logger.info("Extracted section length: %d", len(section))
        return section

    def parse_section(self, section, response):
        for label_element in section.css(self.extractor.label_css):
            label = self.extractor.extract_label(label_element)
            if label:
                content = self.extractor.extract_content(label_element, response)
                if content:
                    yield self.format_item(label, content)

    def format_item(self, label, content):
        return {
            'label': label,
            'content': content,
        }
       
