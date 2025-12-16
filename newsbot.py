'''
✅TODO: load config
TODO: schedule checking for new items every 15 min
✅TODO: fetch rss content from each links in the library
    ✅TODO: for each item in the rss list
        ✅TODO: check release time of the new items, only process the news articles released within 15 mins
        ✅TODO: format rss news item (title, link, published date, channel, webhook url)
        ✅TODO: crawl the news article
        TODO: translate by AI
        TODO: send to discord

'''
import os
from dotenv import load_dotenv
from config.rss_settings import RssLibrary
import traceback
import asyncio
import sys
from datetime import datetime, timezone, timedelta
import aiohttp
import feedparser
from crawler import Crawler
load_dotenv()

class NewsBot:
    CHECK_INTERVAL = 30800  # 3 hours
    REQUEST_TIMEOUT = 30
    TIMEZONE = 'America/Toronto'
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    AI_MODEL = 'gemini-2.5-flash'
    
    def __init__(self):
        self.rss_library = RssLibrary()
        self.session = None
        self.is_running = False
        self.crawler = Crawler()
    
    async def start(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.REQUEST_TIMEOUT)
        )
        self.is_running = True
        
        for rss_link in self.rss_library.library:
            
            channel = rss_link.channel
            webhock_url = rss_link.webhook_url
            
            all_rss_feeds = await self.fetch_rss(rss_link)
            filtered_rss_feeds = self.filter_updated_rss(all_rss_feeds)
            if len(filtered_rss_feeds) == 0:
                return
            
            urls_to_scrape = [ rss_feed.link for rss_feed in filtered_rss_feeds]
            
            for url in urls_to_scrape:
                markdown_contents = await self.crawler.scrape(url)
                
            #     # use AI to translate the page
            #     # send the result to discord


        
    async def stop(self):
        print('🛑 Stopping Multi-Feed News Bot...')
        self.is_running = False
        
        if self.session:
            await self.session.close()
        
    async def fetch_rss(self, rss_link):
        ''' 
        Fetch rss content from a rss object using feedparser, return a list of dictionary, each distionary represent a rss feed 
        Args:
            rss: Rss object
        Return:
            all_rss_feeds: a list of dictionary
        '''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/rss+xml, application/xml, text/xml, application/atom+xml, */*',
        }
        
        print(f'📡 Fetching {rss_link.name}: {rss_link.url}')
        async with self.session.get(rss_link.url, headers=headers) as response:
            if response.status != 200:
                raise Exception(f'HTTP {response.status}')
            content = await response.text()
        feed = feedparser.parse(content)
        all_rss_feeds = feed.entries

        print(f'📰 Fetched {len(all_rss_feeds)} RSS items from { rss_link.name}')
        
        return all_rss_feeds

                
    def filter_updated_rss(self, all_rss_feeds):
        ''' 
        Filter rss news item base on 'published' attribute of each item in the list, only return the item that is release within CHECK_INTERVAL
        Args:
            all_rss_feeds: a list of dictionary
        return:
            filtered_rss_feed: a list of dictionary
        '''
        now = datetime.now(timezone.utc)
        delta = timedelta(seconds=self.CHECK_INTERVAL)
        filtered_rss_feed = []
        for feed in all_rss_feeds:
            pub_date = feed.get('published', '')
            if pub_date and ((now - datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %z')) < delta):
                filtered_rss_feed.append(feed)
        print(f'📰 Found {len(filtered_rss_feed)} new RSS items')
        return filtered_rss_feed

                
async def main():
    bot = NewsBot()
    
    try:
        await bot.start()
        await bot.stop()
    except Exception as error:
        print(f'❌ Failed to start bot: {error}')
        traceback.print_exc()
        await bot.stop()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())