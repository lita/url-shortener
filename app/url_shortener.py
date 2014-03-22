import requests
from redis import Redis

class UrlManager(object):
    """
    Handles generating the url shortener and keeping track of the database.
    """
    redis = Redis()
    
    @staticmethod
    def initalize():
        if not UrlManager.redis.exists('count'):
            UrlManager.redis.set('count', 0)

    @staticmethod
    def processUrl(url):
        count = UrlManager.redis.get('count')
        if not url.startswith('http://'):
            url = 'http://' + url
        try:
            result = requests.get(url)
        except requests.exceptions.RequestException:
            return False
        if result.status_code >= 400:
            return False
        count = int(count) + 1
        UrlManager.redis.set(count, url)
        UrlManager.redis.set('count', count)
        return count

    @staticmethod
    def getUrl(key):
        return UrlManager.redis.get(key)
