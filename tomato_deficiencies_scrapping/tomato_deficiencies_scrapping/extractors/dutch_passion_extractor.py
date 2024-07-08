from .base_extractor import BaseExtractor

class DutchPassionExtractor(BaseExtractor):
    def extract_label(self, element):
        label_element = element.css('::text').get()
        if label_element:
            return label_element.strip()
        return None

    def extract_content(self, label_element, response):
        content = []
        next_element = label_element.xpath('./following-sibling::*')
        for element in next_element:
            if element.xpath('name()').get() in self.config.stop_labels:
                break
            images = self.extract_images(element, response)
            texts = element.xpath(self.config.text_xpath).extract()
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
            caption = self.extract_caption(img)
            images.append({'image_url': response.urljoin(img_src), 'caption': caption})
        return images if images else None

    def extract_caption(self, img):
        caption_element = img.xpath('./following-sibling::p[1]//text()').get()
        if caption_element:
            return caption_element.strip()
        return None
