import asyncio
from datetime import datetime
from src.core.models.collector_jobs import CollectorJobsEntity


def ListingsJob(Base):

    class Job(Base):

        def __init__(self) -> None:
            super().__init__()
            self.rows = None
            self.load_more = False
            self.last_modified_date = None
            self.counter = 1

        @property
        def runner_timeout(self):
            # 10 minutes
            return 600

        @property
        def last_modified_field(self):
            return 'updated'

        @property
        def last_modified_param(self):
            return 'since'

        @property
        def max_row_count(self):
            return 100

        @property
        def job_name(self):
            return '%s.listings_job' % self.name

        def get_params(self):
            if not self.last_modified_date:
                return {}
            return {
                self.last_modified_field: self.last_modified_date
            }

        async def dispatch(self, name, row):
            if (self.queue):
                await self.queue.publish(row)

        def filter_result(self, result):
            return result

        def pre_process(self, row):
            return row

        def transformer(self, row):
            return row

        async def process(self):
            for row in self.rows:
                row = self.pre_process(row)
                transformed = self.transformer(row)
                await self.dispatch(self.job_name, transformed)

        def calculate_paginate(self):
            entity = CollectorJobsEntity({
                'service': self.name
            })

            try:
                entity.fetch()
            except:
                pass

            if entity.row.get('id') and entity.row['fetch_counter'] < self.max_row_count:
                self.last_modified_date = entity.row['last_modified_date']
                self.load_more = True

            return entity

        def save_job(self, job_entity):
            last = self.rows[-1][self.last_modified_field]
            if not job_entity.row.get('id'):
                job_entity.row = {
                    'service': self.name,
                    'job_name': self.job_name,
                    'has_more': True,
                    'fetch_counter': 1,
                    'last_modified_date': last,
                    'updated_at': datetime.now()
                }

                job_entity.new()
                self.load_more = True
                return job_entity

            job_entity.row['fetch_counter'] += 1
            job_entity.row['last_modified_date'] = last
            job_entity.sync()
            self.load_more = job_entity.row['fetch_counter'] < self.max_row_count
            return job_entity

        async def execute(self):
            # entity = self.calculate_paginate()
            self.fetch()
            self.rows = self.filter_result(self.data)
            self.last_modified_date = self.rows[-1][self.last_modified_field]
            self.counter += 1
            # self.save_job(entity)
            await self.process()
            if self.counter < self.max_row_count:
                await self.execute()

        def reset(self):
            self.counter = 1
            self.last_modified_date = None

        async def run(self):
            while True:
                await self.execute()
                self.reset()
                await asyncio.sleep(self.runner_timeout)

    return Job
