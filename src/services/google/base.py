from src.core.rest_job import RestJob
from src.config import config


class GoogleBaseJob(RestJob):

    @property
    def name(self):
        return 'GOOGLE'

    @property
    def url(self):
        return f'https://serpapi.com/search.json?engine=google_jobs&api_key={config.serpapi_key}'
