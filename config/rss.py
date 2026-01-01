'''
Classes:
    RssLirary: a class that hold each rss source as an object
        Attr:  
            library: contain a list of rss object
        method:
            add_rss

    Rss: a class represent a rss srouce
        Attr:
            name
            url
            channel
            webhook_url

'''

import os
from dotenv import load_dotenv
from config.feeds import FEEDS

load_dotenv()

class Rss:
    CANADA = 'canada-news'
    WORLD = 'world-news'
    TEST = 'test'
    
    ALL_CHANNELS = ['canada-news', 'world-news', 'test']
    
    def __init__(self, name: str, url: str, channel: str):
        self.name = name
        self.url = url
        if channel not in self.ALL_CHANNELS:
            raise ValueError("Channel must be either 'canada-news', 'world-news', or 'test' ")
        self.channel = channel
        if channel == self.CANADA:
            self.webhook_url = os.getenv('CANADA_NEWS_WEBHOOK_URL')
        elif  channel == self.WORLD:
            self.webhook_url = os.getenv('WORLD_NEWS_WEBHOOK_URL')
        elif channel == self.TEST:
            self.webhook_url = os.getenv('TEST_WEBHOOK_URL')
    def __str__(self):
        return f"Name: {self.name}, url: {self.url}, Channel: {self.channel}"

class RssLibrary:
    
    def __init__(self):
        self.library: list[Rss] = []
        for feed in FEEDS:
            self.add_rss(feed['name'], feed['url'], feed['channel'])
    
    def add_rss(self, name: str, url: str, channel: str):
        rss = Rss(name, url, channel)
        self.library.append(rss)
        
if __name__ =="__main__":
    lib = RssLibrary()
    for item in lib.library:
        print(item)