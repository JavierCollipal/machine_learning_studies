def dutch_passion_parse(spider, response):
    section = response.css(spider.extractor.section_css)
    if section:
        for label_element in section.css(spider.extractor.label_css):
            label = spider.extractor.extract_label(label_element)
            if label:
                content = spider.extractor.extract_content(label_element, response)
                if content:
                    yield {
                        'label': label,
                        'content': content,
                    }