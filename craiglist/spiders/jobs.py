# -*- coding: utf-8 -*-
import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['newyork.craigslist.org']
    start_urls = ['http://newyork.craigslist.org/search/egr']

    def parse(self, response):
        # jobs = response.xpath('//a[@class="result-title hdrlnk"]/text()').extract()
        # for job in jobs:
        #     yield {'Job ':job}

        listings = response.xpath('//li[@class="result-row"]')

        for listing in listings:
            time = listing.xpath('.//*[@class="result-date"]/@datetime').extract_first()
            name = listing.xpath('.//*[@class="result-title hdrlnk"]/text()').extract_first()
            link = listing.xpath('.//*[@class="result-title hdrlnk"]/@href').extract_first()

            # yield {
            #     'Time':time,
            #     'Job': name,
            #     'Link': link
            # }

            yield scrapy.Request(link,
                                 callback=self.parse_listing,
                                 meta={'time':time, 'name':name, 'link':link})
        next_page_url = response.xpath('//a[@class="button next"]/@href').extract_first()

        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url), callback = self.parse)

    def parse_listing(self, response):
        time = response.meta['time']
        name = response.meta['name']
        link = response.meta['link']

        images = response.xpath('//*[@class="thumb"]/@href').extract()

        conpensation = response.xpath('//*[@class="attrgroup"]/span[1]/b/text()').extract_first()
        type_of_job = response.xpath('//*[@class="attrgroup"]/span[2]/b/text()').extract_first()

        description = response.xpath('//*[@id="postingbody"]/text()').extract()

        yield {
            'time':time,
            'name':name,
            'link':link,
            'images':images,
            'conpensation':conpensation,
            'type_of_job':type_of_job,
            'description':description
        }


