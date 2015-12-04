import redis
class Schedule:
    def __init__(self,listname):
        self.conn=redis.Redis(host='localhost', port=6379, db='0')
        self.list=listname

    def push(self,x):
        self.conn.lpush(self.list,x)

    def request_url(self):
        x=self.conn.rpop(self.list)
        if x:
            print x
            #self.request_url()
            return x

        else:
            return -1

    def get_all(self):
        len=self.conn.llen(self.list)
        print len
        print self.conn.lrange(self.list,start=0,end=len)
    def pop_all(self):
        next_url=self.request_url()
        while next_url!=-1:
            print next_url
            next_url=self.request_url()

#s=Schedule(listname='list')
# for i in range(1,100):
#     s.push(i)
#s.get_all()
#s.request_url()