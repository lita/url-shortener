import unittest

from redis import Redis

from app.url_shortener import UrlManager
from flask import Flask


class UrlShortenerTestCase(unittest.TestCase):

    def setUp(self):
        # Setup Dev Server, which is set to db=1
        
        app = Flask(__name__)
        # Load in the config file
        app.config.from_object('config')

        UrlManager.redis = Redis(db=1, port=app.config['DB_PORT'])
        UrlManager.redis.set(1, 'http://www.google.com')
        UrlManager.redis.set(2, 'http://www.facebook.com')
        UrlManager.redis.set('count', '2')

    def testProcessUrlFail(self):
        self.assertFalse(UrlManager.processUrl('sdkjfskdjfdlsjfsldk'))

    def testProcessUrlSuccess(self):
        self.assertEqual(UrlManager.processUrl('www.google.com'), '3')
        self.assertEqual(UrlManager.processUrl('http://www.google.com'), '4')
        longUrl = ('https://www.google.com/maps/place/455+Broadway/@40.72078,-' 
                   '74.001119,17z/data=!3m1!4b1!4m2!3m1!1s0x89c2598bd3a41ddb:0x' 
                   '696f7383cb54af4d')

        self.assertEqual(UrlManager.processUrl(longUrl), '5')

    def testUrlKey(self):
        self.assertEqual(UrlManager.getUrl('1'), 'http://www.google.com')

    def testGenerateor(self):
        UrlManager.generateMappings()
        self.assertEqual(UrlManager.numToChar[0], '0')
        self.assertEqual(UrlManager.numToChar[9], '9')
        self.assertEqual(UrlManager.numToChar[10], 'a')
        self.assertEqual(UrlManager.numToChar[35], 'z')
        self.assertEqual(UrlManager.numToChar[36], 'A')
        self.assertEqual(UrlManager.numToChar[61], 'Z')

        self.assertEqual(UrlManager.charToNum['0'], 0)
        self.assertEqual(UrlManager.charToNum['9'], 9)
        self.assertEqual(UrlManager.charToNum['a'], 10)
        self.assertEqual(UrlManager.charToNum['z'], 35)
        self.assertEqual(UrlManager.charToNum['A'], 36)
        self.assertEqual(UrlManager.charToNum['Z'], 61)

    def testGenerateKey(self):
        self.assertEqual(UrlManager.generateKey(63), '11')
        self.assertEqual(UrlManager.generateKey(62), '01')
        self.assertEqual(UrlManager.generateKey(6), '6')
        self.assertEqual(UrlManager.generateKey(10), 'a')
        self.assertEqual(UrlManager.generateKey(62), '01')
        self.assertEqual(UrlManager.generateKey(124), '02')
        self.assertEqual(UrlManager.generateKey(61), 'Z')

    def testConvertToNum(self):
        self.assertEqual(UrlManager.convertToNum('11'), 63)
        self.assertEqual(UrlManager.convertToNum('01'), 62)
        self.assertEqual(UrlManager.convertToNum('02'), 124)
        self.assertEqual(UrlManager.convertToNum('a'), 10)
        self.assertEqual(UrlManager.convertToNum('Z'), 61)

    def tearDown(self):
        UrlManager.redis.flushdb()

if __name__ == '__main__':
    unittest.main()