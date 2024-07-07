import scrapy

class DeficienciesSpider(scrapy.Spider):
    name = 'deficiencies'
    start_urls = ['https://dutch-passion.com/en/blog/a-visual-guide-to-cannabis-deficiencies-n987']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})

    def parse(self, response):
        self.logger.info("Parsing page: %s", response.url)
        for section in response.css('div#blog-item-content'):
            self.logger.debug("Found section: %s", section.get())
            for deficiency in section.css('h3, h2'):
                label = self.extract_label(deficiency)
                self.logger.debug("Extracted label: %s", label)
                if label:
                    images = self.extract_images(deficiency, response)
                    self.logger.debug("Extracted images: %s", images)
                    if images:
                        yield {
                            'label': label,
                            'images': images,
                        }

    def extract_label(self, deficiency):
        label_element = deficiency.css('::text').get()
        if label_element:
            return label_element.strip()
        return None

    def extract_images(self, deficiency, response):
        images = []
        # Find images in the current section
        for img in deficiency.xpath('./following-sibling::img'):
            img_src = img.css('::attr(src)').get()
            caption = self.extract_caption(img)
            images.append({'image_url': response.urljoin(img_src), 'caption': caption})
        
        # Find images in the next paragraph elements
        for img in deficiency.xpath('./following-sibling::p[img]/img'):
            img_src = img.css('::attr(src)').get()
            caption = self.extract_caption(img)
            images.append({'image_url': response.urljoin(img_src), 'caption': caption})

        return images if images else None

    def extract_caption(self, img):
        caption_element = img.xpath('./following-sibling::p[1]//text()').get()
        if caption_element:
            return caption_element.strip()
        return None
