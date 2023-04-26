from src.core.rest_job import RestJob
from src.config import config


class IdealistBaseJob(RestJob):

    @property
    def name(self):
        return 'IDEALIST'

    @property
    def auth(self):
        return (config.idealist_token, '')

    @property
    def url(self):
        return 'https://www.idealist.org/api/v1'
