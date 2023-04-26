from src.core.listings import ListingsJob
from src.core.worker import Worker
from ..idealist import IdealistBaseJob
from .transforms import job_transformer
from src.jobs.listings import ListingWorker


class IdealistListingJob(ListingsJob(IdealistBaseJob)):

    def __init__(self) -> None:
        super().__init__()
        self.queue = IdealistRowQueue()

    @property
    def path(self):
        return '/listings/jobs'

    def filter_result(self, result):
        return result['jobs']


class IdealistRowQueue(Worker(IdealistBaseJob)):

    def __init__(self):
        super().__init__()
        self.queue = ListingWorker()

    @property
    def name(self):
        return 'IDEALIST.Listings'

    @property
    def path(self):
        return '/listings/jobs/%s' % self.get_id()

    def filter_result(self, result):
        return result['job']

    @property
    def subject(self):
        return 'listing'

    def transformer(self, row):
        return job_transformer(row)
