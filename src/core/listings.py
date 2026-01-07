import asyncio
from datetime import datetime
from typing import Optional, Any, List
from src.core.models.collector_jobs import CollectorJobsEntity
from src.utils.datadog import push_metric
from src.utils.logger import get_logger

logger = get_logger('listings')


def ListingsJob(Base):

    class Job(Base):

        def __init__(self) -> None:
            super().__init__()
            self.rows: Optional[List[Any]] = None
            self.load_more: bool = False
            self.last_modified_date: Optional[str] = None
            self.counter: int = 1
            self.limit: int = 20
            self.offset: int = 0

        @property
        def runner_timeout(self) -> int:
            # 20 hours (configurable)
            return 72000

        @property
        def last_modified_field(self) -> str:
            return 'updated'

        @property
        def last_modified_param(self) -> str:
            return 'since'

        @property
        def max_row_count(self) -> int:
            return 50

        @property
        def job_name(self) -> str:
            return '%s.listings_job' % self.name

        def get_last_modified_date(self) -> Optional[str]:
            if not self.rows or len(self.rows) < 1:
                return None
            return self.rows[-1][self.last_modified_field]

        def get_params(self) -> dict:
            if not self.rows:
                return {}
            return {
                self.last_modified_param: self.get_last_modified_date()
            }

        async def dispatch(self, name: str, row: dict) -> None:
            if (self.queue):
                await self.queue.publish(row)

        def filter_result(self, result: Any) -> List[Any]:
            return result

        def pre_process(self, row: dict) -> dict:
            return row

        def transformer(self, row: dict) -> dict:
            return row

        async def process(self) -> None:
            for row in self.rows:
                row = self.pre_process(row)
                transformed = self.transformer(row)
                await self.dispatch(self.job_name, transformed)

        def calculate_paginate(self) -> CollectorJobsEntity:
            entity = CollectorJobsEntity({
                'service': self.name
            })

            try:
                entity.fetch()
            except Exception as err:
                logger.error(f"Error fetching collector job entity: {err}")

            if entity.row.get('id') and entity.row['fetch_counter'] < self.max_row_count:
                self.last_modified_date = entity.row['last_modified_date']
                self.load_more = True

            return entity

        def save_job(self, job_entity: CollectorJobsEntity) -> CollectorJobsEntity:
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

        async def execute(self) -> None:
            """
            Execute the listing job using iteration instead of recursion.
            This prevents potential stack overflow for large datasets.
            """
            while self.counter <= self.max_row_count:
                try:
                    self.fetch()
                    self.rows = self.filter_result(self.data)

                    if not self.rows:
                        logger.info(f'{self.name} no more results at page {self.counter}')
                        break

                    push_metric(self.job_name, len(self.rows))
                    await self.process()

                    logger.info(f'{self.name} fetched page {self.counter} with {len(self.rows)} rows')

                    self.counter += 1
                    self.offset += self.limit

                except Exception as err:
                    logger.error(f'{self.name} error on page {self.counter}: {err}')
                    # Break on error to prevent infinite retry loops
                    break

        def reset(self) -> None:
            self.counter = 1
            self.offset = 0
            self.last_modified_date = None
            self.rows = None

        async def run(self) -> None:
            logger.info(f'Starting {self.job_name}')
            while True:
                try:
                    await self.execute()
                except Exception as err:
                    logger.error(f'{self.job_name} run error: {err}')
                self.reset()
                logger.info(f'{self.job_name} sleeping for {self.runner_timeout}s')
                await asyncio.sleep(self.runner_timeout)

    return Job
