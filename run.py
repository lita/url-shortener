#!flask/bin/python
import pickle

from app import app
from app.url_shortener import UrlManager

def generateFakeData():
    adminKey = "PDY4Ns9OFmZmaaJdooChhlwtKHQ="
    ips = ['74.212.183.186', '199.27.128.0', '64.233.173.205']

    with open('ip_test.txt', 'r') as f:
        for i in f:
            if i.startswith('#'):
                continue
            ips.append(i.strip())

    UrlManager.redis.set(adminKey, pickle.dumps(ips))

generateFakeData()
app.run(host='0.0.0.0',port=8000,debug = True)