import urllib3
import json
import subprocess
from variables import httpLinks
from variables import httpHeaders


class HttpFunctions:

    @staticmethod
    def apipost(link, body):
        http = urllib3.PoolManager()
        print(link, body)
        r = http.request('POST', "%s%s" % (httpLinks.DOMAIN, link), body=body,
                         headers=httpHeaders.JSON_HEADERS)
        try:
            data = json.loads(r.data.decode("utf-8"))
        except:
            data = r.data.decode("utf-8")
        return r, data

    @staticmethod
    def apiget(link, body):
        http = urllib3.PoolManager()
        print(link,body)
        r = http.request('GET', "%s%s" % (httpLinks.DOMAIN, link),
                         fields=body,
                         headers=httpHeaders.ACCEPTHEADERS)
        try:
            data = json.loads(r.data.decode("utf-8"))
        except:
            data = r.data.decode("utf-8")
        return r, data

    @staticmethod
    def apiput(link, body):
        http = urllib3.PoolManager()
        r = http.request('PUT', "%s%s" % (httpLinks.DOMAIN, link), body=body,
                         headers=httpHeaders.JSONHEADERS)
        try:
            data = json.loads(r.data.decode("utf-8"))
        except:
            data = r.data.decode("utf-8")
        return r, data

    @staticmethod
    def apidelete(link, body):
        print(link, body)
        http = urllib3.PoolManager()
        r = http.request('DELETE', "%s%s" % (httpLinks.DOMAIN, link),
                         fields=body,
                         headers=httpHeaders.ACCEPTHEADERS)
        try:
            data = json.loads(r.data.decode("utf-8"))
        except:
            data = r.data.decode("utf-8")
        return r, data

    @staticmethod
    def apipath(link, body):
        http = urllib3.PoolManager()
        r = http.request('PATH', "%s%s" % (httpLinks.DOMAIN, link), body=body,
                         headers=httpHeaders.JSONHEADERS)
        try:
            data = json.loads(r.data.decode("utf-8"))
        except:
            data = r.data.decode("utf-8")
        return r, data

    @staticmethod
    def getPostgresIP():
        docker_config = json.loads(subprocess.run(["docker", "inspect", "backend_db_1"],
                                                  check=True,
                                                  stdout=subprocess.PIPE,
                                                  universal_newlines=True).stdout)
        ip = str(docker_config[0]["NetworkSettings"]["Networks"]["backend_default"]["IPAddress"])
        return ip

    @staticmethod
    def getBackendIP():
        docker_config = json.loads(subprocess.run(["docker", "inspect", "backend_backend_1"],
                                                  check=True,
                                                  stdout=subprocess.PIPE,
                                                  universal_newlines=True).stdout)
        ip = str(docker_config[0]["NetworkSettings"]["Networks"]["backend_default"]["IPAddress"])
        return ip
