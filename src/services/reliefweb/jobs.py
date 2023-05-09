from src.core.listings import ListingsJob
from src.core.queues import Queue
from .base import ReliefwebBaseJob
from .transforms import job_transformer
from src.services.socious.listings import ListingWorker


class ReliefwebListingJob(ListingsJob(ReliefwebBaseJob)):

    def __init__(self) -> None:
        super().__init__()
        self.queue = ReliefwebRowQueue()

    def get_params(self):
        params = {
            'appName': 'socious',
            'profile': 'full',
            'limit': self.limit,
            'offset': self.offset
        }
        return params

    @property
    def job_name(self):
        return '%s.listings_job' % self.name

    def filter_result(self, result):
        return result['data']


class ReliefwebRowQueue(Queue(ReliefwebBaseJob)):

    def __init__(self):
        super().__init__()
        self.queue = ListingWorker()

    @property
    def name(self):
        return 'RELIEFWEB.Listings'

    @property
    def path(self):
        return '/%s' % self.get_id()

    def filter_result(self, result):
        return result['data'][0]

    @property
    def subject(self):
        return 'RELIEFWEB.Listings'

    def transformer(self, row):
        return job_transformer(row)
