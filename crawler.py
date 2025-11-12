from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import PruningContentFilter
import asyncio

class Crawler:

    def __init__(self):
        self.browser_conf = BrowserConfig(
            browser_type="chromium",
            headless=True,
            verbose=True
        )
   
        self.markdown_generator = DefaultMarkdownGenerator(
            content_filter=PruningContentFilter(threshold=0.5,threshold_type="fixed"),
            options={"ignore_links": True}
        )
        
        self.run_conf = CrawlerRunConfig(
            cache_mode = CacheMode.BYPASS,
            markdown_generator=self.markdown_generator,
            word_count_threshold=10,
        )
            
    async def scrape_many(self, urls):
        try:
            async with AsyncWebCrawler(config=self.browser_conf) as crawler:
                results = await crawler.arun_many(
                    urls,
                    config=self.run_conf
                )
                if len(results) != 0:
                    fit_markdown = [result.markdown.fit_markdown for result in results]                    
                    print('✅ Scraping successful')
                    return fit_markdown
                else:
                    raise Exception('Scraping failed - no content returned')
            
        except Exception as error:
            print(f'❌ Crawl4AI error for {urls}: {error}')

if __name__ == "__main__":
    async def main():
        crawler = Crawler()
        result = await crawler.scrape(["https://www.geeksforgeeks.org/python/python-features/"])
        with open("fit_markdown_geeksforgeeks.txt.", "w", encoding='utf-8') as f:
            f.write(str(result))        
        
    asyncio.run(main())
        