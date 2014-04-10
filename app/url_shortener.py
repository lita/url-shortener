import hashlib
import base64
import pickle

import requests
from redis import Redis

class UrlManager(object):
    """
    Handles generating the url shortener and keeping track of the database.
    """
    @classmethod
    def initalize(cls, app):
        cls.app = app
        cls.redis = Redis(port=app.config['DB_PORT'])
        if not cls.redis.exists('count'):
            cls.redis.set('count', 0)
        cls.base = 62
        cls.generateMappings()

    @classmethod
    def generateMappings(cls):
        cls.numToChar = {}
        cls.charToNum = {}
        count = 0
        for i in xrange(cls.base):
            if i < 10:
                char = chr(ord('0')+i)
                cls.numToChar[i] = chr(ord('0')+i)
                cls.charToNum[chr(ord('0')+i)] = i
            if i >= 10 and i <= 35:
                offset = 10
                char = chr(ord('a')+(i-offset))
                cls.numToChar[i] = char
                cls.charToNum[char] = i
            if i >= 36:
                offset = 36
                char = chr(ord('A')+(i-offset))
                cls.numToChar[i] = char
                cls.charToNum[char] = i

    @classmethod
    def processUrl(cls, url):
        """
        Generates a id with the count. Stores the website into the database.
        TODO: need to handle the case of giving itself to the shortener
        """
        count = cls.redis.get('count')
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url
        try:
            result = requests.get(url)
        except Exception as err:
            return False
        if result.status_code >= 400:
            return False
        count = int(count) + 1
        
        cls.redis.set('count', count)
        key = cls.generateKey(count)
        adminKey = cls.generateAdminKey(key)
        cls.redis.set(count, pickle.dumps((url, adminKey)))
        return key, adminKey

    @classmethod
    def getUrl(cls, key, request):
        id = cls.convertToNum(key)
        url, adminKey = pickle.loads(cls.redis.get(id))
        ip = request.remote_addr
        if cls.redis.exists(adminKey):
            ipHisotry = pickle.loads(redis.get(adminKey))
            ipHisotry.append(ip)
        else:
            ipHisotry = [ip]
        cls.redis.set(adminKey, pickle.dumps(ipHisotry))

        return url

    @classmethod
    def getAdminData(cls, adminKey):
        return pickle.loads(cls.redis.get(adminKey))

    @classmethod
    def convertToNum(cls, key):
        id = 0
        power = 0
        while key != '':
            char = key[0]
            id += cls.charToNum[char] * cls.base**power
            power += 1
            key = key[1:]

        return id

    @classmethod
    def generateKey(cls, id):
        """
        Converts the id to 62 base key so that the id is not guessable.
        Converts to little endian for performance
        """
        digits = []
        while id > 0:
            remainder = id % cls.base
            digits.append(cls.numToChar[remainder])
            id = id/cls.base
        return ''.join(digits)

    @classmethod
    def generateAdminKey(cls, key):
        hash_key = base64.b64encode(hashlib.sha1(key).digest())
        return hash_key


