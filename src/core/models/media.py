from . import BaseEntity
from src.core.db import DB
from .consts import *


class MediaEntity(BaseEntity):

    @property
    def fetch_query_name(self):
        return 'get_media'

    @property
    def fetch_query_params(self):
        return (self.row['id'])

    @property
    def sync_query_name(self):
        return 'insert_media'

    @property
    def columns(self) -> tuple:
        return (
            'id',
            'identity_id',
            'filename',
            'url'
        )
