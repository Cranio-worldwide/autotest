import urllib3
import json
import variables
from variables import httpLinks
from variables import httpHeaders


class HttpFunctions:

    @staticmethod
    def apipost(link,body):
        http = urllib3.PoolManager()
        r = http.request('POST', "%s%s" % (httpLinks.DOMAIN, link), body=body,
                         headers=httpHeaders.JSONHEADERS)
        data = json.loads(r.data.decode("utf-8"))
        return r, data
