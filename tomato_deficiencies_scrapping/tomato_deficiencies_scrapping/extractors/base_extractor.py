class BaseExtractor:
    def __init__(self, section_css, label_css, image_css, config):
        self.section_css = section_css
        self.label_css = label_css
        self.image_css = image_css
        self.config = config

    def extract_label(self, element):
        raise NotImplementedError("extract_label must be implemented by subclasses")

    def extract_content(self, label_element, response):
        raise NotImplementedError("extract_content must be implemented by subclasses")

    def extract_images(self, element, response):
        raise NotImplementedError("extract_images must be implemented by subclasses")
