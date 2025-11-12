from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import PruningContentFilter
import asyncio

class Crawler:
    ''' crawl individual news article page'''
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
       
        self.crawler = AsyncWebCrawler(config=self.browser_conf)
        
    async def start(self):
        await self.crawler.start()
        
    async def close(self):
        await self.crawler.close()
        
    async def scrape(self, urls):
        try:
            results = await self.crawler.arun_many(
                urls,
                config=self.run_conf
            )
            
            for result in results:
                if result.success and result.markdown:
                    print('✅ Scraping successful')
                    return result.markdown.fit_markdown
                else:
                    raise Exception('Scraping failed - no content returned')
                
        except Exception as error:
            print(f'❌ Crawl4AI error for {urls}: {error}')

if __name__ == "__main__":
    async def main():
        crawler = Crawler()
        await crawler.start()
        result = await crawler.scrape(["https://www.geeksforgeeks.org/python/python-features/"])
        with open("fit_markdown_reult.txt.", "w") as f:
            f.write(result)        
        await crawler.close()
        
    asyncio.run(main())
        