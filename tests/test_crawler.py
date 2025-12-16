from crawler import Crawler
import pytest

@pytest.fixture
def crawler(scope = "module"):
    return Crawler()

@pytest.mark.asyncio
async def test_scrape_many(crawler):
    results = await crawler.scrape_many(["https://en.wikipedia.org/wiki/Python_(programming_language)", "https://en.wikipedia.org/wiki/History_of_Python"])
    assert isinstance(results, list)
    assert "Guido van Rossum" in results[0]
    assert "Guido van Rossum" in results[1]
    
@pytest.mark.asyncio
async def test_scrape(crawler):
    result = await crawler.scrape("https://en.wikipedia.org/wiki/Python_(programming_language)")
    assert "Guido van Rossum" in result
