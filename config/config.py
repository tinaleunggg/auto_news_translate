'''
Config file:
- system config
- time zone
- api keys
- rss links

'''
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):

        self.GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
        self.AI_MODEL = 'gemini-2.5-flash'
        self.CHECK_INTERVAL = 300  # 5 minutes in seconds
        self.MAX_STORED_TITLES = 1000
        self.REQUEST_TIMEOUT = 30
        self.TIMEZONE = 'America/Toronto'
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'info')
        
        self._print_config()
    
    def _print_config(self):
        print('📝 Configuration loaded:')
        print(f'   RSS Feeds: {len(self.RSS_FEEDS)} configured')
        for feed in self.RSS_FEEDS:
            print(f'     - {feed["name"]} → {feed["channel"]}')
        print(f'   Timezone: {self.TIMEZONE}')
        print(f'   AI Model: {self.AI_MODEL}')
        print(f'   Check Interval: {self.CHECK_INTERVAL}s')