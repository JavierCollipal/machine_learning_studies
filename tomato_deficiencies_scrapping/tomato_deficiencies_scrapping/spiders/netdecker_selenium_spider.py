import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NetdeckerSpider(scrapy.Spider):
    name = "netdecker_spider"
    start_urls = ["http://www.store.netdecker.cl/11-material-sellado"]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=10,
                wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, 'a.button.ajax_add_to_cart_button.exclusive'))
            )

    def parse(self, response):
        driver = response.meta.get('driver')

        if driver:
            try:
                # Wait for the "Añadir al carro" button to be clickable and click it
                add_to_cart_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.button.ajax_add_to_cart_button.exclusive'))
                )
                add_to_cart_button.click()

                # Wait for the cart update (assuming there's some visual change or alert)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".cart_block"))
                )

                # Extract data after clicking the button
                products = response.css('.ajax_block_product')
                for product in products:
                    yield {
                        'name': product.css('h3 a::text').get(),
                        'price': product.css('.price::text').get(),
                        'availability': product.css('.availability::text').get(),
                    }
            except Exception as e:
                self.logger.error(f"Error during Selenium interaction: {e}")
        else:
            self.logger.error("WebDriver instance not found in response.meta")
