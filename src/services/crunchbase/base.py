from src.core.rest_job import RestJob
from src.config import config


class CrunchBaseJob(RestJob):

    @property
    def method(self):
        return 'POST'

    @property
    def name(self):
        return 'CRUNCHBASE'

    @property
    def headers(self):
        return {
            'X-cb-user-key': config.crunchbase_api_key,
            'content-type': 'application/json'
        }

    @property
    def url(self):
        return f'https://api.crunchbase.com/v4/data/searches/organizations'
