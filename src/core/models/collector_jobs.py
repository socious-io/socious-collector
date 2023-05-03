from . import BaseEntity
from src.core.db import DB
from .consts import *


class CollectorJobsEntity(BaseEntity):

    @property
    def sync_skip_id(self):
        return False

    @property
    def fetch_query_name(self):
        return 'get_collector_job'

    @property
    def fetch_query_params(self):
        return (self.row['service'], self.row['job_name'])

    @property
    def sync_query_name(self):
        return 'update_collector_job'

    @property
    def new_query_name(self):
        return 'new_collector_job'

    @property
    def columns(self) -> tuple:
        return (
            'service',
            'job_name',
            'has_more',
            'fetch_counter',
            'last_modified_date',
            'updated_at',
            'id'
        )
