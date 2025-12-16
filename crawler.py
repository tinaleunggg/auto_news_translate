from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import PruningContentFilter
import asyncio

class Crawler:

    def __init__(self):
        ''' Setting up crawl4ai web crawler '''
        
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

    ''' better to run asyn crawler to crwal article one by one, when one finish, it can go to next step. 
    run a for loop in newsbot, start multiple parallet crawler and then AI request'''
    
    async def scrape(self, url):
        '''
        scrape one article
        
        :param self: the Crawler instance 
        :param url: a url strings
        
        '''
        try:
            async with AsyncWebCrawler(config=self.browser_conf) as crawler:
                result = await crawler.arun(
                    url,
                    config=self.run_conf
                )
                if not result.success:
                    raise ValueError('Scraping failed - no content returned')
                
                fit_markdown = result.markdown.fit_markdown                    
                print('✅ Scraping successful')
                return fit_markdown

        except Exception as error:
            print(f'❌ Crawl4AI error for {url}: {error}')
    
    
    
    async def scrape_many(self, urls):
        '''
        Docstring for scrape_many
        
        :param self: the Crawler instance 
        :param urls: a list of url strings
        
        '''
        try:
            async with AsyncWebCrawler(config=self.browser_conf) as crawler:
                results = await crawler.arun_many(
                    urls,
                    config=self.run_conf
                )
                fit_markdowns = []
                for result in results:
                    if result.success:
                        print(f"Just completed: {result.url}")
                        fit_markdowns.append(result.markdown.fit_markdown)
                    else:
                        print("Scraping failed - no content returned") 
                  
                print(f'✅ Scraping successful for {len(fit_markdowns)} urls')
                return fit_markdowns
            
        except Exception as error:
            print(f'❌ Crawl4AI error for {urls}: {error}')

if __name__ == "__main__":
    async def main():
        crawler = Crawler()
        result = await crawler.scrape("https://www.geeksforgeeks.org/python/python-features/")
        with open("fit_markdown_geeksforgeeks.txt.", "w", encoding='utf-8') as f:
            f.write(str(result))        
        
    asyncio.run(main())
        