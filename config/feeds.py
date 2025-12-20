'''
FEEDS contain a list of rss dictionary
{
    'name': name,
    'url': url,
    'channel': must be either 'canada-news' or 'world-news'
}
'''

FEEDS = [
            {
                'name': 'Global News Canada',
                'url': 'https://globalnews.ca/canada/feed/',
                'channel': 'canada-news',
            },
            {
                'name': 'CBC Canada',
                'url': 'https://www.cbc.ca/webfeed/rss/rss-canada',
                'channel': 'canada-news',
            },
            {
                'name': 'CBC British Columbia',
                'url': 'https://www.cbc.ca/webfeed/rss/rss-canada-britishcolumbia',
                'channel': 'canada-news',
            },
            {
                'name': 'CBC world news',
                'url': 'https://www.cbc.ca/webfeed/rss/rss-world',
                'channel': 'world-news',
            }
        ]

if __name__ =="__main__":
    for item in FEEDS:
        print(item)