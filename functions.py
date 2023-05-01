import urllib3
import json
from variables import httpLinks
from variables import httpHeaders


class HttpFunctions:

    @staticmethod
    def apipost(link, body):
        http = urllib3.PoolManager()
        r = http.request('POST', "%s%s" % (httpLinks.DOMAIN, link), body=body,
                         headers=httpHeaders.JSONHEADERS)
        data = json.loads(r.data.decode("utf-8"))
        return r, data

    @staticmethod
    def apiget(link, body):
        http = urllib3.PoolManager()
        r = http.request('GET', "%s%s" % (httpLinks.DOMAIN, link),
                         fields=body,
                         headers=httpHeaders.JSONHEADERS)
        data = json.loads(r.data.decode("utf-8"))
        return r, data

    @staticmethod
    def apiput(link, body):
        http = urllib3.PoolManager()
        r = http.request('PUT', "%s%s" % (httpLinks.DOMAIN, link), body=body,
                         headers=httpHeaders.JSONHEADERS)
        data = json.loads(r.data.decode("utf-8"))
        return r, data

    @staticmethod
    def apidelete(link, body):
        http = urllib3.PoolManager()
        r = http.request('DELETE', "%s%s" % (httpLinks.DOMAIN, link),
                         fields=body,
                         headers=httpHeaders.JSONHEADERS)
        data = json.loads(r.data.decode("utf-8"))
        return r, data

    @staticmethod
    def apipath(link, body):
        http = urllib3.PoolManager()
        r = http.request('PATH', "%s%s" % (httpLinks.DOMAIN, link), body=body,
                         headers=httpHeaders.JSONHEADERS)
        data = json.loads(r.data.decode("utf-8"))
        return r, data


