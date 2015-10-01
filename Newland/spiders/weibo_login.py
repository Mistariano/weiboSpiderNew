# encoding: utf-8
import sys
import urllib2
import urllib
import cookielib
import os
import lxml.html as HTML
import pymongo
#
# supporting Chinese
reload(sys)
sys.setdefaultencoding("utf-8")
#
class Fetcher(object):
    def __init__(self):

        self.conn = pymongo.MongoClient()
        self.db = self.conn.weibo
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                        'Referer':'','Content-Type':'application/x-www-form-urlencoded'}
        self.cookiefiles=[]
        print 'the Fetcher has been created'


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

    def do_login(self,username,pwd,filename):
        cj = cookielib.LWPCookieJar()
        cookie_processor = urllib2.HTTPCookieProcessor(cj)
        opener = urllib2.build_opener(cookie_processor, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        print 'do_login with username:',username
        print 'and pwd:',pwd
        #url = 'http://3g.sina.com.cn/prog/wapsite/sso/login.php?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%D0%C2%C0%CB%CE%A2%B2%A9&vt='
        url='http://login.weibo.cn/login/'
        rand, passwd, vk ,bt,sb= self.get_rand(url)
        data = urllib.urlencode({'mobile': username,
                                 passwd: pwd,
                                 'remember': 'on',
                                 'backURL': 'http://weibo.cn/',
                                 'backTitle': bt,
                                 'vk': vk,
                                 'submit': sb,
                                 'encoding': 'utf-8'})
        url = 'http://login.weibo.cn/login/' + rand
        req = urllib2.Request(url, data, self.headers)
        print'1'
        resp = urllib2.urlopen(req)
        page = resp.read()
        link = HTML.fromstring(page).xpath("//a/@href")[0]
        if not link.startswith('http://'): link = 'http://weibo.cn/%s' % link
        req = urllib2.Request(link, headers=self.headers)
        result=urllib2.urlopen(req)
        #print result.read()
        print'2'
        print'filename:',filename
        cj.save(filename=filename)
        print 'login success'

    def fetch(self, url):
        print 'fetch url: ', url
        req = urllib2.Request(url, headers=self.headers)
        return urllib2.urlopen(req).read()

    def login(self):
        for i in range(1,self.db.account.count()+1):
            a=self.db.account.find({'_id':i})[0]
            print 'check cookies No.',i
            un=a['username']
            pwd=a['pwd']
            print'username:',un
            print'pwd:',pwd
            filename='cookies/'+str(i)+'.dat'
            self.cookiefiles.append(filename)
            if os.path.exists(filename):
                print 'has existed'
            else:
                print 'now loading...'
                self.do_login(username=un,pwd=pwd,filename=filename)
        print 'cookiefiles:'
        for ck in self.cookiefiles:
            print ck
        return self.cookiefiles







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


