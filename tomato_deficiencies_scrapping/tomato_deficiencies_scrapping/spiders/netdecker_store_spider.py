import scrapy


class NetdeckerSpider(scrapy.Spider):
    name = "netdecker_store"
    allowed_domains = ["store.netdecker.cl"]
    start_urls = ["http://www.store.netdecker.cl/11-material-sellado"]

    def parse(self, response):
        for product in response.css("ul#product_list li.ajax_block_product"):
            yield {
                "name": product.css("h3 a::text").get(),
                "url": product.css("h3 a::attr(href)").get(),
                "image": product.css("a.product_img_link img::attr(src)").get(),
                "description": product.css("p.product_desc a::text").get(),
                "price": product.css("span.price::text").get(),
                "availability": product.css("span.availability::text").get(),
            }

        # Follow pagination links
        next_page = response.css("li#pagination_next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
