import pytest
from newsbot import NewsBot
from config.rss import Rss, RssLibrary
from ai_translator import AiTranslator
from tests.test_ai_translator import response_body
import aiohttp
import datetime
from aioresponses import aioresponses
import json
from email.utils import format_datetime
from unittest.mock import patch, AsyncMock, MagicMock


@pytest.fixture(scope = "module")
def rss():
    return Rss("test", "https://test_rss", "test")

@pytest.fixture(scope = "module")
def newsbot(rss):
    newsbot = NewsBot()
    new_library = RssLibrary()
    new_library.library = [rss]
    newsbot.rss_library = new_library
    return newsbot

@pytest.fixture
def mock_aioresponse():
    with aioresponses() as mock:
        yield mock
        
@pytest.fixture
def mock_crawler():
    # patch the crawler.AsyncWebCrawler, whenever you call this object, it will be replaced by the mock object
    # context manager to provide a scope you want to apply the mock
    with patch("crawler.AsyncWebCrawler", autospec=True) as MockCrawler:
        crawler_instance = MockCrawler.return_value.__aenter__.return_value
        crawler_instance.arun = AsyncMock()
        crawler_instance.arun_many = AsyncMock()
        yield crawler_instance

@pytest.fixture
def mock_result():
    # MagicMock() mock a dictionary, or other container object
    result = MagicMock()
    result.success = True
    markdown = MagicMock()
    markdown.fit_markdown = "test result"
    result.markdown = markdown
    return result

@pytest.mark.asyncio
async def test_fetch_rss(newsbot, rss, mock_aioresponse):
    mock_aioresponse.get(
        rss.url,
        status=200,
        body=mock_rss_xml,
        headers={"Content-Type": "application/rss+xml"},
    )
    async with aiohttp.ClientSession() as session:
        response = await newsbot.fetch_rss(rss, session)
        assert type(response) == list

def test_parse_pubdate(newsbot):
    assert isinstance(newsbot.parse_pub_date("Wed, 19 Apr 2023 12:44:51 GMT"), datetime.datetime)
    assert isinstance(newsbot.parse_pub_date("Wed, 31 Dec 2025 22:12:05 +0000"), datetime.datetime)

@pytest.mark.asyncio
async def test_filter_rss(newsbot, rss, mock_aioresponse):
    mock_aioresponse.get(
        rss.url,
        status=200,
        body=mock_rss_xml,
        headers={"Content-Type": "application/rss+xml"},
    )
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
async def test_process_article(newsbot, rss, mock_aioresponse, mock_crawler, mock_result):
    mock_crawler.arun.return_value = mock_result
    mock_aioresponse.post(AiTranslator.API_URL, status=200, payload=json.loads(response_body))
    mock_aioresponse.post(rss.webhook_url, status=204)
    async with aiohttp.ClientSession() as session:
        assert await newsbot.process_article(rss.url, "test title", "test pub date", "test", "test channel", rss.webhook_url, session) == True

@pytest.mark.asyncio
async def test_process_rss(newsbot, rss, mock_aioresponse):
    mock_aioresponse.get(
        rss.url,
        status=200,
        body=mock_rss_xml,
        headers={"Content-Type": "application/rss+xml"},
    )
    mock_aioresponse.post(AiTranslator.API_URL, status=200, payload=json.loads(response_body))
    mock_aioresponse.post(rss.webhook_url, status=204)
    async with aiohttp.ClientSession() as session:
        assert await newsbot.process_rss(rss, session) == True

now = datetime.datetime.now()
pub_date = format_datetime(now)
mock_rss_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
    <channel>
        <title>Mock RSS Feed</title>
        <link>https://www.example.com/</link>
        <description>This is a mock RSS feed for testing.</description>
        <item>
        <title>Test Article 1</title>
        <link>https://www.example.com/article1</link>
        <description>This is a short description for article 1.</description>
        <pubDate>{pub_date}</pubDate>
        <guid>https://www.example.com/article1</guid>
        </item>
    </channel>
    </rss>"""