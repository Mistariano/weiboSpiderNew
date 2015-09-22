__author__ = 'MisT'
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request,FormRequest
from scrapy import log
from Newland.items import WeiboItem
#import weibo_login
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
            #login()
            #self.login_cookie = read_cookie()
            self.login_cookie={'gsid_CTandWM':'4ukBf0c41Qf10dqbMa4tinNJZf1','SUHB':'0WGsnX0DCd1ary','SUB':'_2A257BGxEDeTxGeNI7FAW9S_FyD2IHXVYB3QMrDV6PUJbrdAKLVnXkW1rfd8i3eEd8reMOriQ_YOxQWFoGw..','_T_WM':'d3a36aad1f5c53eaa5debf09fe307523'}
            #yield Request(url='http://weibo.cn/5672751931/follow?vt=1',cookies=self.login_cookie,callback=self.get_user)

            for i in range(1,25):
                hot_url = "http://weibo.cn/pub/topmblog?page="+str(i)
                yield Request(url=hot_url,callback=self.parse_hot,cookies=self.login_cookie,meta=
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
                #'''
                if(self.handle_url(url)):
                #'''
                    yield Request(url=url,cookies=self.login_cookie,callback=self.parse_user,meta=
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
                yield Request(url='http://weibo.cn/comment/'+urlid,cookies=self.login_cookie,callback=self.parse_comnt,meta={'nick':response.meta['nick'],'id':urlid})
            yield Request(url=response.url+'/follow',cookies=self.login_cookie,callback=self.get_user)
            yield Request(url=response.url+'/fans',cookies=self.login_cookie,callback=self.get_user)

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
    def get_user(self,response):
        log.msg("get_user:"+response.url , level=log.INFO)
        try:

            users=Selector(text=response.body).xpath('//tr/td[@valign="top"][2]').extract()
            for user in users:
                sel=Selector(text=user)
                url=sel.xpath('//a/@href').extract()[0]
                nick=sel.xpath('//a/text()').extract()[0]
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

'''
functions of old versions
def read_cookie():
    log.msg("reading cookie... " , level=log.INFO)
    cookie_file = "weibo_login_cookies.dat"
    cookie_jar = cookielib.LWPCookieJar(cookie_file)
    cookie_jar.load(ignore_discard=True, ignore_expires=True)
    cookie = dict()
    for ck in cookie_jar:
        cookie[ck.name] = ck.value
    log.msg("done " , level=log.INFO)
    return cookie

def login():
    log.msg("login... " , level=log.INFO)
    username = 'mist_weibo_1@163.com'
    pwd = 'hdlhdl'
    cookie_file = 'weibo_login_cookies.dat'
    fet=weibo_login.Fetcher(username=username,pwd=pwd)
    return fet.login(cookie_filename=cookie_file)
'''
