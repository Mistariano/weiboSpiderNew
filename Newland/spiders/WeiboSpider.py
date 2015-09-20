__author__ = 'MisT'
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import log
from Newland.items import WeiboItem
class WeiboSpider(scrapy.Spider):
    name="weibo"
    allowed_domains = ["weibo.cn"]
    def start_requests(self):
        log.msg("start" , level=log.INFO)
        try:
            for i in range(1,25):
                hot_url = "http://weibo.cn/pub/topmblog?page="+str(i)
                yield Request(url=hot_url,callback=self.parse_hot,meta=
                {
                    #'dont_redirect': True,
                    #'handle_httpstatus_list': [302]
                })
        except Exception, e:
            log.msg("Fail to start" , level=log.ERROR)
            log.msg(str(e), level=log.ERROR)

    def parse_hot(self,response):
        log.msg("parse_hot:"+response.url , level=log.INFO)
        try:
            sel=Selector(text=response.body)
            users=sel.xpath('//a[@class="nk"]').extract()
            for user in users:
                sel=Selector(text=user)
                url=sel.xpath('//@href').extract()[0]
                nick=sel.xpath('//text()').extract()[0]
                #print nick,url
                yield Request(url=url,callback=self.parse_user,meta=
                {
                    'nick':nick,
                    #'dont_redirect': True,
                    #'handle_httpstatus_list': [302]
                })
        except Exception, e:
            log.msg("Fail to parse_hot" , level=log.ERROR)
            log.msg(str(e), level=log.ERROR)

    def parse_user(self,response):
        log.msg("parse_user:"+response.url , level=log.INFO)
        try:
            sel=Selector(text=response.body)
            urlids=sel.xpath('//div[@class="c"]/@id').re('M_(.*)')
            for urlid in urlids:
                yield Request(url='http://weibo.cn/comment/'+urlid,callback=self.parse_comnt,meta={'nick':response.meta['nick'],'id':urlid})
        except Exception, e:
            log.msg("Fail to parse_user" , level=log.ERROR)
            log.msg(str(e), level=log.ERROR)

    def parse_comnt(self,response):
        log.msg("parse_comnt:"+response.url , level=log.INFO)
        try:
            sel=Selector(text=response.body)
            text=sel.xpath('//div[@id="M_"]//span[@class="ctt"]/text()').extract()
            time=sel.xpath('//div[@id="M_"]//span[@class="ct"]/text()').extract()
            item=WeiboItem(text=text,time=time,user=response.meta['nick'])
            yield item
        except Exception, e:
            log.msg("Fail to parse_comnt" , level=log.ERROR)
            log.msg(str(e), level=log.ERROR)
