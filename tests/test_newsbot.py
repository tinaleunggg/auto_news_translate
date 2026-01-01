import pytest
from newsbot import NewsBot
from config.rss import Rss, RssLibrary
import aiohttp
import datetime
from aioresponses import aioresponses

@pytest.fixture(scope = "module")
def newsbot():
    newsbot = NewsBot()
    new_library = RssLibrary()
    new_library.library = [Rss("test", "https://lorem-rss.herokuapp.com/feed", "test")]
    newsbot.rss_library = new_library
    return newsbot

@pytest.fixture(scope = "module")
def rss():
    return Rss("test", "https://lorem-rss.herokuapp.com/feed", "test")

@pytest.fixture
def mock_aioresponse():
    with aioresponses() as m:
        yield m

@pytest.mark.asyncio
async def test_fetch_rss(newsbot, rss):
    async with aiohttp.ClientSession() as session:
        response = await newsbot.fetch_rss(rss, session)
        assert type(response) == list

def test_parse_pubdate(newsbot):
    assert isinstance(newsbot.parse_pub_date("Wed, 19 Apr 2023 12:44:51 GMT"), datetime.datetime)
    assert isinstance(newsbot.parse_pub_date("Wed, 31 Dec 2025 22:12:05 +0000"), datetime.datetime)

@pytest.mark.asyncio
async def test_filter_rss(newsbot, rss):
    async with aiohttp.ClientSession() as session:
        response = await newsbot.fetch_rss(rss, session)
        assert type(newsbot.filter_updated_rss(response)) == list

@pytest.mark.asyncio
async def test_send_to_discord(newsbot, rss):
    async with aiohttp.ClientSession() as session:
        response = await newsbot.send_to_discord(rss.url, "test title", "test pub date", "test content", "test", "test channel", rss.webhook_url, session)
        assert response.status == 204

@pytest.mark.asyncio
async def test_fail_send_to_discord(newsbot, rss, mock_aioresponse):
    mock_aioresponse.post("https://testing", status=500)
    with pytest.raises(aiohttp.ClientResponseError):
        async with aiohttp.ClientSession() as session:    
            await newsbot.send_to_discord(rss.url, "test title", "test pub date", "test content", "test", "test channel", "https://testing", session)
         
@pytest.mark.asyncio
async def test_process_article(newsbot, rss):
    pass       
            
@pytest.mark.asyncio
async def test_process_rss(newsbot, rss):
    pass