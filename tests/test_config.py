import pytest
from config.rss import Rss, RssLibrary
import os
from dotenv import load_dotenv
from config.feeds import FEEDS

@pytest.fixture
def env_var(scope = "module"):
    load_dotenv()

def test_feed():
    assert type(FEEDS) == list
    for item in FEEDS:
        assert item['name']
        assert item['url']
        assert item['channel']

def test_rss():
    cbc = Rss("test", "http://testing", "world-news")
    assert cbc.name == "test"
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
    rss_library = RssLibrary()
    for item in rss_library.library:
        assert isinstance(item, Rss)