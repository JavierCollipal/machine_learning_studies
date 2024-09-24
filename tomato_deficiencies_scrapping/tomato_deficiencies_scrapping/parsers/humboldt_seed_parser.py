# humboldt_seed_parser.py

def humboldt_seed_parse(spider, response):
    section = response.css(spider.extractor.section_css)
    labels = section.css(spider.extractor.label_css).getall()
    images = section.css(spider.extractor.image_css).getall()
    content = spider.extractor.extract_content(section)

    yield {
        'url': response.url,
        'labels': labels,
        'images': images,
        'content': content,
    }
