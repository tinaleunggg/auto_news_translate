from crawler import Crawler
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from crawl4ai import CrawlResult, MarkdownGenerationResult

@pytest.fixture
def crawler(scope = "module"):
    return Crawler()

@pytest.fixture
def mock_crawler():
    with patch("crawler.AsyncWebCrawler", autospec=True) as MockCrawler:
        crawler_instance = MockCrawler.return_value.__aenter__.return_value
        crawler_instance.arun = AsyncMock()
        crawler_instance.arun_many = AsyncMock()
        yield crawler_instance

@pytest.fixture
def mock_result():
    result = MagicMock()
    result.success = True
    markdown = MagicMock()
    markdown.fit_markdown = "test result"
    result.markdown = markdown
    return result

@pytest.fixture
def mock_result1():
    result = MagicMock()
    result.success = True
    markdown = MagicMock()
    markdown.fit_markdown = "test result1"
    result.markdown = markdown
    return result


@pytest.mark.asyncio
async def test_scrape_many(crawler, mock_crawler, mock_result, mock_result1):
    mock_crawler.arun_many.return_value = [mock_result, mock_result1]
    
    results = await crawler.scrape_many(["http://testing", "http://testing"])
    assert isinstance(results, list)
    assert "test result" in results[0]
    assert "test result1" in results[1]
    
    
@pytest.mark.asyncio
async def test_scrape_mock(crawler, mock_crawler, mock_result):
    mock_crawler.arun.return_value= mock_result
    result = await crawler.scrape("http://testing")
    assert result == "test result"
