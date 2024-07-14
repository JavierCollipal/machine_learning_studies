import scrapy

class NetdeckerAddToCartSpider(scrapy.Spider):
    name = 'netdecker_add_to_cart'
    start_urls = ['http://www.store.netdecker.cl/']

    def parse(self, response):
        # Add the logic to parse the product pages and add to cart
        products = response.css('.product-container')
        for product in products:
            product_page = product.css('a.product_img_link::attr(href)').get()
            if product_page:
                yield response.follow(product_page, self.parse_product_page)

    def parse_product_page(self, response):
        # Add the logic to click the "Añadir al carro" button
        add_to_cart_form = response.css('form#buy_block')
        if add_to_cart_form:
            form_data = {
                'id_product': add_to_cart_form.css('input[name=id_product]::attr(value)').get(),
                'quantity': 1,
                'add': 'Añadir al carro'
            }
            add_to_cart_url = add_to_cart_form.css('form::attr(action)').get()
            if add_to_cart_url:
                yield scrapy.FormRequest(
                    url=add_to_cart_url,
                    formdata=form_data,
                    callback=self.confirm_added_to_cart,
                    meta={'product_name': response.css('h1[itemprop=name]::text').get()}
                )

    def confirm_added_to_cart(self, response):
        # Confirm that the item was added to the cart
        product_name = response.meta.get('product_name', 'Unknown product')
        cart_confirmation = response.css('#layer_cart .layer_cart_product h2::text').get()
        if cart_confirmation and 'se ha añadido' in cart_confirmation:
            self.log(f"Successfully added {product_name} to cart.")
        else:
            self.log(f"Failed to add {product_name} to cart.")
