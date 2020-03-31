# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from scrapy.http import Request


class ReserveDateSpider(scrapy.Spider):
    name = 'reserve-date'
    allowed_domains = ['ezakupy.tesco.pl']
    start_urls = ['https://ezakupy.tesco.pl/groceries/pl-PL/login']
    base_address = 'https://ezakupy.tesco.pl'
    delivery_url = 'https://ezakupy.tesco.pl/groceries/pl-PL/slots/delivery'

    def parse(self, response):
        token = response.css('body::attr(data-csrf-token)').extract()[0]
        return FormRequest.from_response(response, formdata={
            'onSuccessUrl': '/groceries/pl-PL/',
            'email':  '',
            'password': '',
            '_csrf': token
        }, callback=self.after_login
        , dont_filter=True
        , formxpath='//*[@id="content"]/div/div[1]/div/div[1]/section/div/form')

    def after_login(self,response):
        print('TUUUU0')
        return Request(self.delivery_url,
                        callback = self.start_scraping
                       )


    def start_scraping(self, response):
        print('TUUUU1')
        print(response.url)
        print('URLS')
        next_urls = response.css('.slot-selector--week-tabheader > a::attr(href)').extract()
        for next_url in next_urls: 
            print(self.base_address + next_url)
            yield Request(self.base_address + next_url,
                        callback = self.dates_tab
                       )
    
        yield 'aa'

    def dates_tab(self, response):
        allowed_to_reserve = response.css('.slot-grid--item.available span::text')
        date = response.css('.slot-selector--3-week-tab-space.active a::text').extract_first().strip()

        if allowed_to_reserve: 
            print('ALERT THERE IS DELIVERY for ' + date + ' ' + allowed_to_reserve.extract_first().strip())
        else:
            print('Brak wolnych terminów dla ' + date)
       
       