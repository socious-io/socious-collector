from src.config import config
from src.core.listings import ListingsJob
from src.core.queues import Queue
from .base import AdzunaBaseJob
from .transforms import job_transformer
from src.services.socious.listings import ListingWorker


class AdzunaListingJob(ListingsJob(AdzunaBaseJob)):

    def __init__(self, country) -> None:
        super().__init__()
        self.queue = ListingWorker()
        self.country = country

    @property
    def job_name(self):
        return f'{self.name}.listings_job.{self.country}'

    def get_params(self) -> dict:
        return config.adzuna

    @property
    def max_row_count(self):
        return 1

    @property
    def path(self):
        return f'/{self.country}/search/{self.counter}'

    def filter_result(self, result):
        return result['results']

    def transformer(self, row):
        return job_transformer(row)
