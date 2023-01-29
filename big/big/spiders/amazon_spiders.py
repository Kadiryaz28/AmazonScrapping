import scrapy
from ..items import BigItem

class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon'
    page_number = 2
    start_urls = ['https://www.amazon.de/s?k=b%C3%BCcher+bestseller+2022&sprefix=b%C3%BCch%2Caps%2C94&ref=nb_sb_ss_ts-doa-p_1_4']
                
    def parse(self, response):

        items = BigItem()

        all_boxes = response.css('.s-widget-spacing-small > .sg-col-inner')
        for boxes in all_boxes:
            product_name = boxes.css('.s-link-style .a-text-normal').css('::text').extract()
            product_author = boxes.css('.a-color-secondary .a-size-base:nth-child(2)').css('::text').extract()
            product_price = boxes.css('.s-price-instructions-style .a-price-whole').css('::text').extract()
            product_imagelink = boxes.css('.s-image::attr(src)').extract()
            product_rating = boxes.css('.a-spacing-top-small .aok-align-bottom').css('::text').extract()
            product_valuation = boxes.css('.a-spacing-top-small .s-link-style .s-underline-text').css('::text').extract()
            product_link = boxes.css('.s-line-clamp-2::attr(href)').get()

            items['product_name'] = product_name
            items['product_author'] = product_author
            items['product_price'] = product_price
            items['product_imagelink'] = product_imagelink
            items['product_rating'] = product_rating
            items['product_valuation'] = product_valuation
            items['product_link'] = 'https://www.amazon.de'+str(product_link)

            yield items

            next_page = 'https://www.amazon.de/s?k=bücher+bestseller+2022&page='+str(AmazonSpiderSpider.page_number)+'&qid=1654968183&sprefix=büch%2Caps%2C94&ref=sr_pg_' + str(AmazonSpiderSpider.page_number)
            if AmazonSpiderSpider.page_number <= 20:
                AmazonSpiderSpider.page_number += 1
                yield response.follow(next_page, callback = self.parse)