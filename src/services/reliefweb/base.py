from src.core.rest_job import RestJob


class ReliefwebBaseJob(RestJob):

    @property
    def name(self):
        return 'RELIEFWEB'

    @property
    def url(self):
        return 'https://api.reliefweb.int/v1/jobs'
