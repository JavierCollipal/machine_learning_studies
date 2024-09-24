def dutch_passion_parse(self, response):
    section = response.css(self.extractor.section_css)
    if section:
        for label_element in section.css(self.extractor.label_css):
            label = self.extractor.extract_label(label_element)
            if label:
                content = self.extractor.extract_content(label_element, response)
                yield format_item(label, content)

def format_item(label, content):
    return {
        'label': label,
        'content': content,
    }