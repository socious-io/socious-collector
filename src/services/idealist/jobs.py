from src.core.listings import ListingsJob
from src.core.queues import Queue
from .base import IdealistBaseJob
from .transforms import job_transformer
from src.services.socious.listings import ListingWorker


class IdealistListingJob(ListingsJob(IdealistBaseJob)):

    def __init__(self, project_type) -> None:
        super().__init__()
        self.queue = IdealistRowQueue(project_type)
        self.project_type = project_type

    @property
    def job_name(self):
        return '%s.listings_job.%s' % (self.name, self.project_type)

    @property
    def path(self):
        return '/listings/%s' % self.project_type

    def filter_result(self, result):
        return result[self.project_type]


class IdealistRowQueue(Queue(IdealistBaseJob)):

    def __init__(self, project_type):
        super().__init__()
        self.queue = ListingWorker()
        self.project_type = project_type

    @property
    def name(self):
        return 'IDEALIST.Listings.%s' % self.project_type

    @property
    def path(self):
        return '/listings/%s/%s' % (self.project_type, self.get_id())

    def filter_result(self, result):
        return result[self.project_type[:-1]]

    @property
    def subject(self):
        return 'IDEALIST.Listings.%s' % self.project_type

    def transformer(self, row):
        return job_transformer(row)
