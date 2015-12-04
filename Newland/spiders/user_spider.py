import scrapy
from scrapy.selector import Selector
from scrapy.http import Request,FormRequest
from scrapy import log
from Newland.items import WeiboItem
from weibo_login import Fetcher
import random
import time
import os
import sys
import redis
import cookielib
import pymongo
# from Newland.schedule import Schedule
#
# class UserSpider(scrapy.Spider)
#     name='user'
#     login_cookies={}
#     cklist=[]
#     s=Schedule('user_list')
#     def start_requests(self):
#         url='http://weibo.cn/tfyiyangqianxi'
#         yield Request(url=url,)
conn = pymongo.MongoClient()
a=[]
b=[]
t0=time.time()
db = conn.weibo['new_user_test2']
for i in range(1,20000):
    a.append(db.find({'_id':i})[0]['mid'])
print time.time()-t0
t0=time.time()
for mid in a:
    b.append( db.find({'mid':mid})[0]['mid'] )
print time.time()-t0

