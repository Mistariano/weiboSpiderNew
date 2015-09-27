__author__ = 'MisT'
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request,FormRequest
from scrapy import log
from Newland.items import WeiboItem
from weibo_login import Fetcher
import os
import cookielib
'''
    This is a crawler for weibo.cn
    ^w^
'''
__version__='v1.0.1'





class WeiboSpider(scrapy.Spider):
    name="weibo"
    allowed_domains = ["weibo.cn"]
    check=['start','ok']
    def start_requests(self):
        log.msg("start" , level=log.INFO)
        try:
            try:
                self.fetcher=Fetcher(username='542058243@qq.com',pwd='hdlhdl',cookie_filename='weibo_cookies.dat')
                self.fetcher.login()
                self.login_cookie = read_cookie()
                print self.login_cookie
            except:
                print 'oh'
            #self.login_cookie={'gsid_CTandWM':'4uDJf0c41dlVGwYhbnfeHnNJZf1'}
            #yield Request(url='http://weibo.cn/tfyiyangqianxi',cookies=self.login_cookie,callback=self.parse_user,meta={'nick':'test'})
            yield Request(url='http://weibo.cn/pub/topmblog?page=2',callback=self.parse_hot,cookies=self.login_cookie)
            #yield Request(url='http://weibo.cn/1768346942/follow',callback=self.get_user,cookies=self.login_cookie)

            '''
            for i in range(1,25):
                hot_url = "http://weibo.cn/pub/topmblog?page="+str(i)
                yield Request(url=hot_url,callback=self.parse_hot,cookies=self.login_cookie,meta=
                {
                    #'dont_redirect': True,
                    #'handle_httpstatus_list': [302]
                })
            '''
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
                #'''
                if(self.handle_url(url)):
                #'''
                    yield Request(url=url,cookies=self.login_cookie,callback=self.parse_user,meta=
                    {
                        'nick':nick

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
            indexes=sel.xpath('//div[@class="c"]/@id').re('M_(.*)')
            for i in indexes:
                yield Request(url='http://weibo.cn/comment/'+i,cookies=self.login_cookie,callback=self.parse_comnt,meta={'nick':response.meta['nick'],'index':i})
            url=sel.xpath('//div[@class="tip2"]').re('<a href="(.*?)follow">.*?</a>')[0]

            #print urls
            #os.system("pause")
            yield Request(url='http://weibo.cn'+url+'follow',cookies=self.login_cookie,callback=self.get_user)
            yield Request(url='http://weibo.cn'+url+'fans',cookies=self.login_cookie,callback=self.get_user)



        except Exception, e:
            log.msg("Fail to parse_user" , level=log.ERROR)
            log.msg(str(e), level=log.ERROR)

    def parse_comnt(self,response):
        log.msg("parse_comnt:"+response.url , level=log.INFO)
        try:
            sel=Selector(text=response.body)
            text=sel.xpath('//div[@id="M_"]//span[@class="ctt"]/text()').extract()
            time=sel.xpath('//div[@id="M_"]//span[@class="ct"]/text()').extract()
            item=WeiboItem(index=response.meta['index'],text=text,time=time,user=response.meta['nick'])
            yield item
        except Exception, e:
            log.msg("Fail to parse_comnt" , level=log.ERROR)
            log.msg(str(e), level=log.ERROR)

    def get_user(self,response):
        log.msg("get_user:"+response.url , level=log.INFO)
        try:

            users=Selector(text=response.body).xpath('//tr/td[@valign="top"][2]').extract()
            #print users
            #os.system("pause")
            for user in users:
                sel=Selector(text=user)
                url=sel.xpath('//a/@href').extract()[0]
                nick=sel.xpath('//a/text()').extract()[0]
                #print url
                #os.system("pause")

                #print 'here?'
                if(self.handle_url(url)):
                    yield Request(url=url,cookies=self.login_cookie,callback=self.parse_user,meta={'nick':nick})
                #print 'here ok'
                #print url,nick
        except Exception, e:
            log.msg("Fail to get_user" , level=log.ERROR)
            log.msg(str(e), level=log.ERROR)

    def handle_url(self,url):
        if url in self.check:
            print url,'is in check'
            return 0

        self.check.append(url)
        print url,'has been insert to check'
        print 'elements:',len(self.check)
        return 1



def read_cookie():
    log.msg("reading cookie... " , level=log.INFO)
    cookie_file = "weibo_cookies.dat"
    cookie_jar = cookielib.LWPCookieJar(cookie_file)
    cookie_jar.load(ignore_discard=True, ignore_expires=True)
    cookie = dict()
    for ck in cookie_jar:
        cookie[ck.name] = ck.value
    log.msg("done " , level=log.INFO)
    return cookie
'''
functions of old versions
def login():
    log.msg("login... " , level=log.INFO)
    username = 'mist_weibo_1@163.com'
    pwd = 'hdlhdl'
    cookie_file = 'weibo_login_cookies.dat'
    fet=weibo_login.Fetcher(username=username,pwd=pwd)
    return fet.login(cookie_filename=cookie_file)
'''
