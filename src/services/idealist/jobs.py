from src.core.listings import ListingsJob
from src.core.queues import Queue
from ..idealist import IdealistBaseJob
from .transforms import job_list_transformer


class IdealistListingJob(ListingsJob(IdealistBaseJob)):

    @property
    def path(self):
        return '/listings/jobs'

    def filter_result(self, result):
        return result['jobs']

    def dispatch(self, name, row):
        Queue(self, row)


class IdealistRowQueue(Queue(IdealistBaseJob)):
    pass
