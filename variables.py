import pytest


class httpHeaders():
    JSONHEADERS = [('User-Agent',
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.124 YaBrowser/22.9.3.886 Yowser/2.5 Safari/537.36"),
           ('Accept', 'application/json'),
           ('Accept-Language', 'ru,en;q=0.9'),
           ('Connection', 'keep-alive'),
           ('Content-Type', 'application/json')]


class httpLinks():
    DOMAIN = "https://backend.princeofprocrastination.art"
    AUTHTOKEN = "/api/v1/auth/token/"