import asyncio


def ListingsJob(Base):

    class Job(Base):

        def __init__(self) -> None:
            super().__init__()
            self.rows = None

        @property
        def runner_timeout(self):
            return 10

        @property
        def job_name(self):
            return '%s.listings_job' % self.name

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

        async def execute(self):
            self.fetch()
            self.rows = self.filter_result(self.data)
            await self.process()

        async def run(self):
            while True:
                await self.execute()
                await asyncio.sleep(self.runner_timeout)

    return Job
