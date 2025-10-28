'''
TODO: load config
TODO: schedule checking for new items every 15 min
TODO: fetch rss content
TODO: check release time of the new items, only process the news articles released within 15 mins
    -> a list of rss news item
    TODO: load news article link
    TODO: crawl the news article
    TODO: translate by AI
    TODO: send to discord

'''
import os
from dotenv import load_dotenv
from config.rss_settings import RssLibrary
load_dotenv()

import traceback
import asyncio
# import json
# import signal
import sys
# from datetime import datetime
# from pathlib import Path
# from typing import Dict, List, Optional, Set
# import xml.etree.ElementTree as ET

import aiohttp
import feedparser
from crawl4ai import AsyncWebCrawler
from dotenv import load_dotenv
# import pytz

# Load environment variables
load_dotenv()

class NewsBot:
    CHECK_INTERVAL = 900  # 15 minutes
    REQUEST_TIMEOUT = 30
    TIMEZONE = 'America/Toronto'
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    AI_MODEL = 'gemini-2.5-flash'
    # LOG_LEVEL = os.getenv('LOG_LEVEL', 'info')
    
    def __init__(self):
        self.rss_library = RssLibrary()
        self.session = None
        self.is_running = False
    
    async def start(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.REQUEST_TIMEOUT)
        )
        self.is_running = True
        await self.check_for_news()
        
    async def stop(self):
        print('🛑 Stopping Multi-Feed News Bot...')
        self.is_running = False
        
        # if self.crawler:
        #     await self.crawler.__aexit__(None, None, None)
        
        if self.session:
            await self.session.close()
        
    async def fetch_rss(self, rss):
        ''' Fetch rss content from a rss object '''

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/rss+xml, application/xml, text/xml, application/atom+xml, */*',
        }
        
        print(f'📡 Fetching {rss.name}: {rss.url}')
        async with self.session.get(rss.url, headers=headers) as response:
            if response.status != 200:
                raise Exception(f'HTTP {response.status}')
            content = await response.text()
        feed = feedparser.parse(content)
        items = feed.entries

        print(f'📰 Found {len(items)} RSS items from {rss.name}')
        
        return items

                
    def filter_rss(self, ):
        ''' Filter rss news item base on released time, only return the item that is release within CHECK_INTERVAL'''
        
    async def check_for_news(self):
        ''' check for news in rss_library'''
        for rss in self.rss_library.library:
            items = await self.fetch_rss(rss)

        

class Crawler:
    ''' crawl individual news article page'''
    def __init__(self):
        self.crawler = AsyncWebCrawler(verbose=True)
    async def start(self):
        await self.crawler.__aenter__()


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