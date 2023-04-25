import requests


class RestJob:

    def __init__(self):
        self.rows = None

    @property
    def url(self):
        return None

    @property
    def path(self):
        return None

    @property
    def auth(self):
        return None

    @property
    def headers(self):
        return {}

    @property
    def method(self):
        return 'GET'

    def dispatch(self, queue, data):
        print(queue, ' ---- > ', data)

    @property
    def proxies(self):
        return dict(http='socks5://localhost:1090',
                    https='socks5://localhost:1090')

    def request(self):
        url = '%s%s' % (self.url, self.path)
        return requests.request(self.method, url, auth=self.auth, headers=self.headers, proxies=self.proxies)

    def fetch(self):
        response = self.request()
        self.rows = self.filter_result(response.json())
        if (response.status_code >= 400):
            raise Exception('response error %s' % str(response.text))
