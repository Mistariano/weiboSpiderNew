# encoding: utf-8
import sys
import os
import pymongo
import datetime
import string
import random
reload(sys)
sys.setdefaultencoding( "utf-8" )
#monthName={1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Eve',12:'Dec'}

class WeiboPipeline(object):
    #def __init__(self):
        #self.file = codecs.open('items.json', 'wb', encoding='utf-8')
    def __init__(self):
        #dispatcher.connect(self.initialize,signals.engine_started)
        #dispatcher.connect(self.finalize,signals.engine_stopped)
        #self.filename='item.sqlite'

        self.conn = pymongo.MongoClient()
        self.db = self.conn.weibo
        self.dbname='item5'



    def process_item(self,item,spider):

        print 'saving data to db >',self.dbname,'<...'
        #id=self.db.item.count()
        id=self.db[self.dbname].count()
        id+=1
        t=handle_time(item['time'])
        self.db[self.dbname].save\
            ({'_id':id,'crawl_id':0,'user':item['user'],'uid':item['uid'],'mid':item['mid'],'text':item['text'],'time':t})
        #print self.db[self.dbname].find({'_id':id})[0]
        print'done[',id,']'
        return item

def handle_time(t):
    t=t.replace(u' ',u'')

    pos_now=t.find(u'刚刚')
    pos_mb=t.find(u'分钟前')
    pos_today=t.find(u'今天')
    pos_m=t.find(u'月')
    #
    if pos_now !=-1:
        ttt=datetime.datetime.now()
        ttt=ttt.strftime("%Y-%m-%d %H:%M")
    elif pos_mb!=-1:
        min=0
        for i in range(0,pos_mb):
            min=min*10+int(t[i])
        delta=datetime.timedelta(minutes=min)
        ttt=datetime.datetime.now()-delta
        ttt=ttt.strftime("%Y-%m-%d %H:%M")
    elif pos_today!=-1:
        ttt=datetime.datetime.now()
        h=int(t[2])*10+int(t[3])
        m=int(t[5])*10+int(t[6])
        ttt.replace(hour=h,minute=m)
        ttt=ttt.strftime("%Y-%m-%d %H:%M")
    elif pos_m!=-1:
        # print'here'
        mon=int(t[pos_m-2])*10+int(t[pos_m-1])
        day=int(t[pos_m+1])*10+int(t[pos_m+2])
        h=int(t[pos_m+4])*10+int(t[pos_m+5])
        min=int(t[pos_m+7])*10+int(t[pos_m+8])
        # print mon,day,h,min
        # os.system("pause")
        ttt=datetime.datetime(year=datetime.datetime.now().year,month=mon,day=day,hour=h,minute=min)
        ttt=ttt.strftime("%Y-%m-%d %H:%M")
        #ttt=datetime.datetime.strftime(u'%m月%d日 %H:%M')
        #08月15日 11:35
    else:
        ttt=t
    # # ttt==time.asctime(ttt)
    #
    # #tm_year,tm_mon,tm_mday,tm_hour,tm_min,tm_sec
    #
    # print'handle:>',t,'<'
    # print 'result:>',ttt,'<'
    return ttt




#handle_time('aaa')

    # def finalize(self):
    #     if self.conn is not None:
    #         self.conn.commit()
    #         self.conn.close()
    #         self.conn=None

    # def create_table(self,filename):
    #     conn=sqlite3.connect(filename)
    #     conn.execute("""create table weiboTable(text,user,time)""")
    #     conn.commit()
    #     return conn

    # def process_item(self, item, spider):
    #     print 'in line'
    #     line = json.dumps(dict(item)) + '\r\n'
    #     self.file.write(line.decode("unicode_escape"))
    #     print 'out line'
    #     return item
    #
    #
    #
    # text = scrapy.Field()
    # user = scrapy.Field()
    # time = scrapy.Field()
    #

# import json
# import codecs
# import sqlite3
# from os import path
# from scrapy import signals
# from scrapy.xlib.pydispatch import dispatcher

# class WeiboPipeline(object):
#     #def __init__(self):
#         #self.file = codecs.open('items.json', 'wb', encoding='utf-8')
#     def __init__(self):
#         self.conn=None
#         dispatcher.connect(self.initialize,signals.engine_started)
#         dispatcher.connect(self.finalize,signals.engine_stopped)
#         self.filename='item.sqlite'
#
#
#     def process_item(self,item,spider):
#         self.conn.execute('insert into weiboTable values(?,?,?)',(item['text'][0],item['user'],item['time'][0]))
#         self.conn.commit()
#         print'done.'
#         return item
#
#
#     def initialize(self):
#         if path.exists(self.filename):
#             self.conn=sqlite3.connect(self.filename)
#         else:
#             self.conn=self.create_table(self.filename)
#
#
#     def finalize(self):
#         if self.conn is not None:
#             self.conn.commit()
#             self.conn.close()
#             self.conn=None
#
#     def create_table(self,filename):
#         conn=sqlite3.connect(filename)
#         conn.execute("""create table weiboTable(text,user,time)""")
#         conn.commit()
#         return conn
#     '''
#     def process_item(self, item, spider):
#         print 'in line'
#         line = json.dumps(dict(item)) + '\r\n'
#         self.file.write(line.decode("unicode_escape"))
#         print 'out line'
#         return item
#
#
#
#     text = scrapy.Field()
#     user = scrapy.Field()
#     time = scrapy.Field()
#     '''
