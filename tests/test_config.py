import pytest
from config.rss_settings import Rss, RssLibrary
from config.rss_feeds import FEEDS
import os
from dotenv import load_dotenv

@pytest.fixture
def env_var(scope = "module"):
    load_dotenv()
    

def test_rss():
    cbc = Rss("cbc", "http://testing", "world-news")
    assert cbc.name == "cbc"
    assert cbc.url == "http://testing"
    assert cbc.channel == "world-news"
    assert cbc.webhook_url == os.getenv('WORLD_NEWS_WEBHOOK_URL')
    
    cbc_canada = Rss("cbc", "http://testing", "canada-news")
    assert cbc_canada.name == "cbc"
    assert cbc_canada.url == "http://testing"
    assert cbc_canada.channel == "canada-news"
    assert cbc_canada.webhook_url == os.getenv('CANADA_NEWS_WEBHOOK_URL')
    
    with pytest.raises(ValueError):    
        rss = Rss("cbc", "http://testing", "sport")

def test_rss_library():
    rss_lib = RssLibrary()
    assert = 