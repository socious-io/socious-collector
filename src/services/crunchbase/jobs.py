from json import dumps
from src.core.listings import ListingsJob
from .base import CrunchBaseJob
from .transforms import job_transformer
from src.services.socious.listings import ListingWorker


class CrunchbaseListingJob(ListingsJob(CrunchBaseJob)):
    def __init__(self):
        super().__init__()
        self.queue = ListingWorker()

    @property
    def job_name(self):
        return '%s.listings_job' % self.name

    @property
    def runner_timeout(self):
        return 60

    @property
    def max_row_count(self):
        return 10

    def get_last_modified_date(self):
        if not self.rows or len(self.rows) < 1:
            return
        return self.rows[-1].get('properties').get('updated_at')

    @property
    def body(self):
        after_id = None
        if self.rows:
            after_id = self.rows[-1].get('uuid')

        return dumps({
            "field_ids": [
                "location_identifiers",
                "website_url",
                "image_url",
                "updated_at",
                'short_description',
                'name'
            ],
            'after_id': after_id
        })

    def filter_result(self, result):
        return result.get('entities')

    def transformer(self, row):
        return job_transformer(row)
