import redis
import threading

class Redis_Listener(threading.Thread):
    def __init__(self, r, channel):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channel)
    
    def channel_data (self, item):
        print item['channel'], ":", item['data']
    
    def run(self):
        for item in self.pubsub.listen():
            if item['data'] == "DIE":
                self.pubsub.unsubscribe()
                print "unsubscribing channel..."
                break
            else:
                self.channel_data(item)

if __name__ == "__main__":
    r = redis.StrictRedis(host="10.0.0.2",port=6379,db=0)
    client = Redis_Listener(r, ['redis_test'])
    client.start()
    
    r.publish('redis_test', 'this will reach the listener')
    
    r.publish('redis_test', 'DIE')
