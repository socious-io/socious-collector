from src.core.db import DB
from .consts import *


class BaseEntity:

    def __init__(self, row: dict):
        self.row = self.clean(row)

    def get_id(self):
        return self.row.get('id')

    @property
    def sync_skip_id(self):
        return True

    @property
    def fetch_query_name(self):
        raise NotImplementedError()

    @property
    def fetch_query_params(self):
        raise NotImplementedError()

    @property
    def sync_query_name(self):
        raise NotImplementedError()

    @property
    def new_query_name(self):
        raise NotImplementedError()

    @property
    def columns(self) -> tuple:
        return ()

    def clean(self, row):
        removeable = []
        for key in row:
            if key not in self.columns:
                removeable.append(key)
        for key in removeable:
            del (row[key])
        return row

    def to_row(self, skip_id=True):
        row = []
        for column in self.columns:
            if skip_id and column == 'id':
                continue
            row.append(self.row.get(column, None))
        return row

    def fetch(self):
        return DB.query(self.fetch_query_name, self.fetch_query_params)[0]

    def sync(self):
        results = DB.query(self.sync_query_name,
                           self.to_row(self.sync_skip_id))
        self.row = results[0]

    def new(self):
        results = DB.query(self.new_query_name, self.to_row())
        self.row = results[0]
