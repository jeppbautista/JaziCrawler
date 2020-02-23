import scrapy
import logging
import urllib.request
import sys
import os.path
import pathlib
from enum import Enum
import json
import requests
import sys; 
print(sys.stdout.encoding)
from JaziCrawler.utils.url_handler import handle_start_urls
from JaziCrawler.utils.preprocess import assign_category
from JaziCrawler.utils.preprocess import filter_out
from DB.db_models.item import Item


# pass arguments to spider using -a command
# Spider arguments are passed while running the crawl command using the -a option.
# For example if i want to pass a domain name as argument to my spider then i will do this-
#
# scrapy crawl myspider -a domain="http://www.example.com"
#
# And receive arguments in spider's constructors:
#
# class MySpider(BaseSpider):
#     name = 'myspider'
#     def __init__(self, domain='', *args, **kwargs):
#         super(MySpider, self).__init__(*args, **kwargs)
#         self.start_urls = [domain]

PRODUCT_NAME = 'div[1]/div[1]/div[2]/div[2]/a/text()'
PRODUCT_URL = 'div[1]/div[1]/div[2]/div[2]/a/@href'

LIMIT = 800

class LazadaSpider(scrapy.Spider):
    name = 'lazada-spider'
    download_delay = 5

    def __init__(self, site='lazada', purpose='dataset', *args, **kwargs):
        logger = logging.getLogger('scrapy.spidermiddlewares.httperror')
        logger.setLevel(logging.ERROR)
        super().__init__(*args, **kwargs)
        logging.getLogger('scrapy').propagate = False

        self.site = site
        self.purpose = purpose
        self.item = Item()
        self.item_counter = {'eyeglasses':0}
        
    def start_requests(self):
        urls = handle_start_urls('lazada')

        for url in urls:  
            try:
                script = """
                    function main(splash)
                        
                        assert(splash:go(splash.args.url))
                        assert(splash:wait(10))
                        return splash:html()
                    end
                """

                yield scrapy.Request(next(iter(url)), self.parse, meta={
                    'splash': {
                        'args': {'lua_source': script},
                        'endpoint': 'execute',
                    }
                })
            except Exception as e:
                print("ERROR :{} at lazada-psider.py Line 126".format(e))       
            # try:
            #     yield scrapy.Request(
            #         next(iter(url)), self.parse,
            #         meta={
            #             'splash': {
            #                 'endpoint': 'render.html',
            #             }
            #         }
            #     )
            # except Exception as x:
            #     print("ERROR :{} at ".format(x), "url")

    def parse(self, response):
        print("===========OUTPUT==============")
        print("CURRENT URL: {}".format(response.url).encode("utf-8"))
        self.item.category = "mug"
        next_page = False
        self.store_as_html(response.body)
        self.item.url = response.url
        # #TODO next_page

        page_counter = 1

        cards = response.css("div[class=c2prKC]")
        # print(cards)

        for card in cards:

            next_page = True
            #self.item.category = assign_category(response.url)

            if self.item.category is None:
                print("Invalid Category")

            else:
                if self.purpose == 'indexing':
                    #TODO indexing
                    pass
                else: 
                    #dataset
                    try:
                        print(self.scrape(card, PRODUCT_NAME)).encode("utf-8")
                        self.item.itemName = self.scrape(card, PRODUCT_NAME)

                        #TODO delete print

                        # print("Current Category: {}".format(self.item.category))
                        # print("Current Item: {}".format(self.item.itemName))

                        if filter_out("lazada", self.item.category, self.item.itemName) == False:
                            self.item.url = self.scrape(card, PRODUCT_URL)
                            self.item.url = response.urljoin(self.item.url)

                            completed = False

                            try:
                                if self.item_counter[self.item.category] < LIMIT:
                                    completed = False
                            except KeyError as e:
                                if self.item.category != 'all-products':
                                    self.debug("Lazada-spider.py : Line 112")
                                pass

                            if self.item.url is None:
                                next_page = True
                                print("Ignore parse_dataset")
                            else:
                                try:
                                    if completed == False:
                                        yield response.follow(self.item.url, callback=self.parse_datasets, meta={'category':self.item.category})
                                    else:
                                        print("Already {} images".format(LIMIT))
                                except Exception as e:
                                    print(e)
                                    self.debug("lazada-spider.py Line 113")
                    except AttributeError:
                        pass
                    except UnicodeError:
                        pass

        
        if next_page:
            x = response.xpath('//li[contains(@class, "ant-pagination-item-active")]')
            next_pagination = (x.xpath("following-sibling::*")[0])
            next_url = next_pagination.xpath("a/@href").extract_first()
            next_url = response.urljoin(next_url)

            print("NEXT URL: {}".format(next_url))
            print("+++++++++++++++++++++++++")

           
            try:
                script = """
                    function main(splash)
                        splash:wait(10)
                        assert(splash:go(splash.args.url))
                        return splash:html()
                    end
                """

                page_counter += 1
                yield scrapy.Request(next_url, self.parse, meta={
                    'splash': {
                        'args': {'lua_source': script},
                        'endpoint': 'execute',
                    }
                })
            except Exception as e:
                print("ERROR :{} at lazada-psider.py Line 126".format(e))


    def parse_datasets(self, response):

        # Current image count

        image_url = response.xpath('//img[contains(@class, "js-taggstar-label-wrapper-img")]/@src').extract_first().strip()
        SKU = response.css("input.sku::attr(value)").extract_first().strip()

        print(response.url)
        print(SKU)
        print()

        # self.item.category = response.meta.get('category')

        # if self.item.category in self.item_counter:
        #     pass
        # else:
        #     self.item_counter.update({self.item.category : 0})

        # counter = int(self.item_counter[self.item.category])
        # if counter >= LIMIT:
        #     if self.is_end() is True:
        #         raise SystemExit(0)
        # else:
        #     pathlib.Path('dataset/{}'.format(self.item.category)).mkdir(parents=True, exist_ok=True) 
        #     temp_path = "dataset/{}/{}.jpg".format(self.item.category,  SKU)

        #     if os.path.exists(temp_path) == False:
        #         urllib.request.urlretrieve(image_url, temp_path)
        #         print("Current URL: {}".format(response.url))
        #         print("Image downloaded: dataset/{}/{}.jpg".format(self.item.category,  SKU))
        #         print("------------------------------------------------------")

        #         counter += 1
        #         self.item_counter[self.item.category] = counter
        #         print(self.item_counter)
        #     else:
        #         print(response.url)
        #         print(temp_path)


    def scrape(self, card, constant):
        return card.xpath(constant).extract_first()

    def debug(self, message):
        print("Message: {}".format(message))

    def get_current_image_count(self, category):
        dir = "{}\\dataset\\{}\\".format(os.getcwd(),category)
        print(dir)
        onlyfiles = next(os.walk(dir))[2]
        return len(onlyfiles)

    def store_as_html(self, body):
        file = "something.html"
        with open (file, 'wb') as f:
            f.write(body)

    def is_end(self):
        for key, value in self.item_counter.items():
            if value < LIMIT:
                return False
        return True


