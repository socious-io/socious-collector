from src.core.rest_job import RestJob
from src.config import config


class AdzunaBaseJob(RestJob):

    @property
    def name(self):
        return 'ADZUNA'

    @property
    def auth(self):
        return (config.idealist_token, '')

    @property
    def url(self):
        return 'https://api.adzuna.com/v1/api/jobs'
