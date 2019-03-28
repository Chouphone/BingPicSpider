from __future__ import absolute_import
import scrapy
import os
import time
import requests
import BingPicSpider.items as items
class BasicSpider(scrapy.Spider):
    
    name = "basic"

    image_count = 1
    search = 'M4+Carbine'
    a = "https://cn.bing.com/images/async?q="
    c = "&first="
    b = "&count=35&relp=35&lostate=r&mmasync=1&dgState=x*175_y*848_h*199_c*1_i*106_r*0&ensearch=1"
    first = 1
    allowed_domains = ['web']
    url = a + search + c + str(first) + b
    #agent = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.165063 Safari/537.36 AppEngine-Google."}
    start_urls = [url]#middle size AK47 search result
    
    #meta = {'dont_redirect': True,  'handle_httpstatus_list': [301, 302]}

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse,dont_filter=True)


    def get_next_url(self):
        self.first = self.first + 35
        return self.a + self.search + self.c + str(self.first) + self.b

    def parse(self, response):
        #self.log("imageurl : %s" % response.xpath('//img/@src').extract())
        item = items.BingpicspiderItem()
        item['image_urls'] = response.xpath('//img/@src').extract()
        imgdow = item['image_urls']
        #download image
        for img in imgdow:
            print("starting save:%d\n", self.image_count)
            print(img[:]) 
            print("\n")
            try:
                time.sleep(2)
                r = requests.get(img[:])
                imgname = "./data/"+ self.search + "_" +str(self.image_count)+ ".jpg"
                with open(imgname, 'wb') as Filewrite:
                    Filewrite.write(r.content)
                self.image_count = self.image_count + 1
            except Exception:
                time.sleep(2)
                print('save Error\n')
            else:
                print("save DONE...")
        time.sleep(15)
        next_url = self.get_next_url()
        print("\n\n\n one down \n\n\n")
        if next_url != None:
            if self.image_count < 5000 and self.first < 6000:
                try:
                    yield scrapy.Request(next_url, callback=self.parse,dont_filter=True)
                except Exception:
                    print("connection Error!\n moving to next page")
                    #self.first = self.first + 1
                    #next_url = self.get_next_url()
                    #yield scrapy.Request(next_url, callback=self.parse,dont_filter=True)

        yield item

        
        
