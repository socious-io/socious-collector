import asyncio
from src.core.listings import ListingsJob
from .base import GoogleBaseJob
from .transforms import job_transformer
from src.services.socious.listings import ListingWorker


class GoogleListingJob(ListingsJob(GoogleBaseJob)):
    def __init__(self):
        super().__init__()
        self.queue = ListingWorker()

    @property
    def job_name(self):
        return '%s.listings_job' % self.name

    @property
    def runner_timeout(self):
        # 10 minutes
        return 60

    def get_params(self):
        params = {
            'q': 'impact',
        }
        return params

    def filter_result(self, result):
        return result.get('jobs_results')

    def transformer(self, row):
        return job_transformer(row)
