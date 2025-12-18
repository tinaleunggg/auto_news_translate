'''
✅TODO: load config
TODO: schedule checking for new items every 15 min
✅TODO: fetch rss content from each links in the library
    ✅TODO: for each item in the rss list
        ✅TODO: check release time of the new items, only process the news articles released within 15 mins
        ✅TODO: format rss news item (title, link, published date, channel, webhook url)
        ✅TODO: crawl the news article
        ✅TODO: translate by AI
        ✅TODO: send to discord

'''
import os
from dotenv import load_dotenv
from config.rss import RssLibrary, Rss
import traceback
import asyncio
import sys
from datetime import datetime, timezone, timedelta
import aiohttp
import feedparser
from crawler import Crawler
from ai_translator import AiTranslator
load_dotenv()

class NewsBot:
    CHECK_INTERVAL = 10000  # 15 mins
    REQUEST_TIMEOUT = 30
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    AI_MODEL = 'gemini-2.5-flash'
    
    def __init__(self):
        self.rss_library = RssLibrary()
        self.session = None
        self.is_running = False
        self.crawler = Crawler()
        self.translator = AiTranslator()
    
    async def start(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.REQUEST_TIMEOUT)
        )
        self.is_running = True
        
        # run a clock, every 15 min do the cycle
        # each article is a asynchronous chain
        try:
            
            for rss in self.rss_library.library:
                channel = rss.channel
                webhock_url = rss.webhook_url
                all_rss_feeds = await self.fetch_rss(rss)
                new_rss_feeds = self.filter_updated_rss(all_rss_feeds)
                if len(new_rss_feeds) == 0:
                    continue
                
                async with asyncio.TaskGroup() as tg:
                    for rss_feed in new_rss_feeds:
                        tg.create_task(
                            self.process_article(rss_feed.link, rss_feed.title, rss_feed.published, rss.name, channel, webhock_url)
                            )

            await self.session.close()
            
        except Exception as error:
            print(error)
            await self.session.close()
            

        
    async def stop(self):
        print('🛑 Stopping Multi-Feed News Bot...')
        self.is_running = False
        
        if self.session:
            await self.session.close()

    async def process_article(self, link: str, title: str, pub_date: str,  name: str, channel: str, webhock_url: str) -> None:
        '''
        pipeline for processing a single raw article link: scrape markdown content, translation by AI and send to discord   
        
        Args:
            link: article url
            title: article title
        Return:
            None
        '''
        markdown_contents = await self.crawler.scrape(link)
        translated_article = await self.translator.process_article(markdown_contents, title, self.session)
        await self.send_to_discord(link, title, pub_date, translated_article, name, channel, webhock_url)
            
            
        
    async def fetch_rss(self, rss_link: Rss) -> list[dict]:
        ''' 
        Fetch rss content from a rss object using feedparser, return a list of dictionary, each distionary represent a rss feed 
        Args:
            rss: Rss object
        Return:
            all_rss_feeds: a list of dictionary from feedparser's feed.entries
        '''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/rss+xml, application/xml, text/xml, application/atom+xml, */*',
        }
        print(f'📡 Fetching {rss_link.name}: {rss_link.url}')
        async with self.session.get(rss_link.url, headers=headers) as response:
            response.raise_for_status()
            feed = feedparser.parse(await response.text())
            all_rss_feeds = feed.entries
        print(f'📰 Fetched {len(all_rss_feeds)} RSS items from { rss_link.name}')
        return all_rss_feeds

                
    def filter_updated_rss(self, all_rss_feeds: list[dict]) -> list[dict]:
        ''' 
        Filter rss news item base on 'published' attribute of each item in the list, only return the item that is release within CHECK_INTERVAL
        Args:
            all_rss_feeds: a list of dictionary from feedparser's feed.entries
        return:
            new_rss_feed: a filtered list of dictionary from feedparser's feed.entries
        '''
        now = datetime.now(timezone.utc)
        delta = timedelta(seconds=self.CHECK_INTERVAL)
        new_rss_feed = []
        for feed in all_rss_feeds:
            pub_date = feed.get('published', '')
            if pub_date and ((now - datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %z')) < delta):
                new_rss_feed.append(feed)
        print(f'📰 Found {len(new_rss_feed)} new RSS items')
        return new_rss_feed

    async def send_to_discord(self, link, title, pub_date, content, name, channel, webhock_url):
        emoji = '🌍' if channel == 'world-news' else '🍁'
        color = 3447003 if channel == 'world-news' else 16711680  # Blue for world, Red for Canada
        
        body = {
            "embeds": [{
                    "title": f"{emoji} {title}",
                    "description": content[:4000] + '...\n\n[內容過長已截斷]' if len(content) > 4000 else content,
                    "color": color,
                    "fields": [
                        {
                            "name": "📅 發布日期",
                            "value": pub_date or '未知',
                            "inline": True
                        },
                        {
                            "name": "📰 新聞來源",
                            "value": name,
                            "inline": True
                        },
                        {
                            "name": "🔗 原文連結",
                            "value": f"[點擊查看完整內容]({link})",
                            "inline": False
                        }
                    ],
                    "footer": {
                        "text": f"頻道: {channel}"
                    },
                    "timestamp": datetime.now().isoformat()
                }]
            }
            
        async with self.session.post(webhock_url, json=body) as response:
            response.raise_for_status()

if __name__ == "__main__":    
    async def main():
        bot = NewsBot()
        try:
            await bot.start()
            await bot.stop()
        except Exception as error:
            traceback.print_exc()
            await bot.stop()
            sys.exit(1)
            
    asyncio.run(main())