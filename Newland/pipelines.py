
import json
import codecs
import sqlite3
from os import path
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

class WeiboPipeline(object):
    #def __init__(self):
        #self.file = codecs.open('items.json', 'wb', encoding='utf-8')
    def __init__(self):
        self.conn=None
        dispatcher.connect(self.initialize,signals.engine_started)
        dispatcher.connect(self.finalize,signals.engine_stopped)
        self.filename='item.sqlite'


    def process_item(self,item,spider):
        self.conn.execute('insert into weiboTable values(?,?,?)',(item['text'][0],item['user'],item['time'][0]))
        self.conn.commit()
        print'done.'
        return item


    def initialize(self):
        if path.exists(self.filename):
            self.conn=sqlite3.connect(self.filename)
        else:
            self.conn=self.create_table(self.filename)


    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn=None

    def create_table(self,filename):
        conn=sqlite3.connect(filename)
        conn.execute("""create table weiboTable(text,user,time)""")
        conn.commit()
        return conn
    '''
    def process_item(self, item, spider):
        print 'in line'
        line = json.dumps(dict(item)) + '\r\n'
        self.file.write(line.decode("unicode_escape"))
        print 'out line'
        return item



    text = scrapy.Field()
    user = scrapy.Field()
    time = scrapy.Field()
    '''
