# encoding: utf-8
import sys
import urllib2
import urllib
import cookielib
import os
import lxml.html as HTML
#
# supporting Chinese
reload(sys)
sys.setdefaultencoding( "utf-8" )
#
class Fetcher(object):
    def __init__(self, username, pwd, cookie_filename):
        print 'check cookies...'
        self.username = username
        self.pwd = pwd
        self.loaded=1
        if os.path.exists(cookie_filename):
            self.loaded=0

        else:
            self.cookie_filename=cookie_filename
        print 'flag:',self.loaded


    def get_rand(self, url):
        headers = {'User-Agent':'Mozilla/5.0 (Windows;U;Windows NT 5.1;zh-CN;rv:1.9.2.9)Gecko/20100824 Firefox/3.6.9',
                   'Referer':''}
        req = urllib2.Request(url ,urllib.urlencode({}), headers)
        resp = urllib2.urlopen(req)
        login_page = resp.read()
        rand = HTML.fromstring(login_page).xpath("//form/@action")[0]
        passwd = HTML.fromstring(login_page).xpath("//input[@type='password']/@name")[0]
        vk = HTML.fromstring(login_page).xpath("//input[@name='vk']/@value")[0]
        bt=HTML.fromstring(login_page).xpath('//input[@name="backTitle"]/@value')[0]
        sb=HTML.fromstring(login_page).xpath('//input[@name="submit"]/@value')[0]
        return rand, passwd, vk,bt,sb

    def do_login(self):
        print 'do_login with username:',self.username
        print 'and pwd:',self.pwd
        #url = 'http://3g.sina.com.cn/prog/wapsite/sso/login.php?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%D0%C2%C0%CB%CE%A2%B2%A9&vt='
        url='http://login.weibo.cn/login/'
        rand, passwd, vk ,bt,sb= self.get_rand(url)
        data = urllib.urlencode({'mobile': self.username,
                                 passwd: self.pwd,
                                 'remember': 'on',
                                 'backURL': 'http://weibo.cn/',
                                 'backTitle': bt,
                                 'vk': vk,
                                 'submit': sb,
                                 'encoding': 'utf-8'})
        url = 'http://login.weibo.cn/login/' + rand
        req = urllib2.Request(url, data, self.headers)
        resp = urllib2.urlopen(req)
        page = resp.read()
        link = HTML.fromstring(page).xpath("//a/@href")[0]
        if not link.startswith('http://'): link = 'http://weibo.cn/%s' % link
        req = urllib2.Request(link, headers=self.headers)
        result=urllib2.urlopen(req)
        #print result.read()
        self.cj.save(filename=self.cookie_filename)
        print 'login success'

    def fetch(self, url):
        print 'fetch url: ', url
        req = urllib2.Request(url, headers=self.headers)
        return urllib2.urlopen(req).read()

    def login(self):
        if self.loaded:
            self.cj = cookielib.LWPCookieJar()
            self.cookie_processor = urllib2.HTTPCookieProcessor(self.cj)
            self.opener = urllib2.build_opener(self.cookie_processor, urllib2.HTTPHandler)
            urllib2.install_opener(self.opener)
            self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                            'Referer':'','Content-Type':'application/x-www-form-urlencoded'}
            self.do_login()




# cookie_file = "weibo_cookies.dat"
# cookie_jar = cookielib.LWPCookieJar(cookie_file)
# cookie_jar.load(ignore_discard=True, ignore_expires=True)
#
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
# urllib2.install_opener(opener)
# url = "http://weibo.cn/"
# print cookie_jar
# result=opener.open(url)
# print result.read()


