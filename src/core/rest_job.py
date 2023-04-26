import requests


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

    def mak_full_url(self):
        return '%s%s' % (self.url, self.path)

    @property
    def proxies(self):
        return dict(http='socks5://localhost:1090',
                    https='socks5://localhost:1090')

    def request(self):
        url = self.mak_full_url()
        return requests.request(self.method, url, auth=self.auth, headers=self.headers, proxies=self.proxies)

    def fetch(self):
        response = self.request()
        if (response.status_code >= 400):
            url = self.mak_full_url()
            raise Exception('response error url=%s  response=%s with status %d' %
                            (url, str(response.text), response.status_code))

        self.data = response.json()
