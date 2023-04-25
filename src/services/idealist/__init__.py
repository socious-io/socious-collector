from src.core.rest_job import RestJob


class IdealistBaseJob(RestJob):

    @property
    def name(self):
        return 'IDEALIST'

    @property
    def url(self):
        return 'https://www.idealist.org/api/v1'

    @property
    def auth(self):
        return ('', '')
