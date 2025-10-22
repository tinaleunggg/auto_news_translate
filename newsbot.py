'''
TODO: load config
TODO: schedule checking for new items every 15 min
TODO: check release time of the new items, only process the item release 15 mins ago
    TODO: load rss links content
    TODO: crawl the news page
    TODO: translate by AI
    TODO: send to discord

'''
import os
from dotenv import load_dotenv
from config.rss_settings import RssLibrary
load_dotenv()


class NewsBot:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    AI_MODEL = 'gemini-2.5-flash'
    CHECK_INTERVAL = 300  # 5 minutes in seconds
    MAX_STORED_TITLES = 1000
    REQUEST_TIMEOUT = 30
    TIMEZONE = 'America/Toronto'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'info')
    
    def __init__(self):
        self.rss_library = RssLibrary()