# humboldt_seed_extractor.py

class HumboldtSeedExtractor:
    def __init__(self, section_css, label_css, image_css, config):
        self.section_css = section_css
        self.label_css = label_css
        self.image_css = image_css
        self.config = config

    def extract_content(self, section):
        content = {}
        current_label = None
        texts = []
        for elem in section.xpath('*'):
            if elem.css(self.label_css).get():
                if current_label:
                    content[current_label] = ' '.join(texts).strip()
                current_label = elem.xpath('string()').get()
                texts = []
            elif elem.css(self.image_css).get():
                img_src = elem.xpath('@src').get()
                if current_label not in content:
                    content[current_label] = []
                content[current_label].append({'type': 'image', 'src': img_src})
            else:
                text = elem.xpath(self.config.text_xpath).getall()
                texts.extend(text)
        
        if current_label:
            content[current_label] = ' '.join(texts).strip()
        
        return content
