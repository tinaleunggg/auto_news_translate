'''
FEEDS contain a list of rss dictionary
{
    'name': name,
    'url': url,
    'channel': must be either 'canada-news' or 'world-news'
}
'''

import os
from dotenv import load_dotenv
load_dotenv()

FEEDS = [
            {
                'name': 'Global News Canada',
                'url': os.getenv('GLOBAL_NEWS_URL'),
                'channel': 'canada-news',
            },
            {
                'name': 'CBC Canada',
                'url': os.getenv('CBC_NEWS_URL'),
                'channel': 'canada-news',
            },
            {
                'name': 'CBC British Columbia',
                'url': os.getenv('CBC_BC_NEWS_URL'),
                'channel': 'canada-news',
            },
            {
                'name': 'CBC world news',
                'url': os.getenv('CBC_WORLD_NEWS_URK'),
                'channel': 'world-news',
            }
        ]

if __name__ =="__main__":
    for item in FEEDS:
        print(item)