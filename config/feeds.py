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
                'name': 'Global News World',
                'url': 'https://globalnews.ca/world/feed/',
                'channel': 'world-news',
            }
        ]