import requests
from src.config import config


class RestJob:

    def __init__(self):
        self.data = None

    @property
    def url(self):
        return None

    @property
    def path(self):
        return ''

    @property
    def auth(self):
        return None

    @property
    def headers(self):
        return {}

    @property
    def method(self):
        return 'GET'

    def get_params(self) -> dict:
        return {}

    def mak_full_url(self):
        return '%s%s' % (self.url, self.path)

    @property
    def proxies(self):
        if not config.http_proxy.get('https') or not config.http_proxy.get('http'):
            return None
        return config.http_proxy

    def request(self):
        url = self.mak_full_url()
        return requests.request(self.method, url, auth=self.auth, headers=self.headers, proxies=self.proxies, params=self.get_params())

    def fetch(self):
        response = self.request()
        if (response.status_code >= 400):
            url = self.mak_full_url()
            raise Exception('response error url=%s  response=%s with status %d' %
                            (url, str(response.text), response.status_code))

        self.data = response.json()
