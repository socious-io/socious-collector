import asyncio
import json
from copy import deepcopy
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrTimeout
from src.config import config
from src.utils.datadog import metrics


lock = asyncio.Lock()


def Queue(Base):

    class Q(Base):
        def __init__(self):
            self.row = {}
            self.nc = NATS()

        @property
        def worker_count(self):
            return 1

        @property
        def name(self):
            return 'queue'

        @property
        def subject(self):
            return 'subject'

        def get_id(self):
            return self.row.get('id')

        def path(self):
            return None

        async def connect(self):
            if self.nc.is_connected:
                return

            options = {
                "servers": [config.nats_url],
                "connect_timeout": 10
            }
            try:
                await self.nc.connect(**options)
                self.connected = True
            except TimeoutError:
                await asyncio.sleep(100)
                await self.connect()

        async def subscribe(self):
            await self.nc.subscribe(self.subject, queue=self.name, cb=self.handler)

        async def dispatch(self, data):
            if (self.queue):
                await self.queue.publish(data)

        async def publish(self, row):
            await self.connect()
            await self.nc.publish(self.subject, json.dumps(row).encode())

        async def handler(self, msg):
            subject = msg.subject
            self.row = json.loads(msg.data.decode())
            metrics.send(metric=self.subject, points=1)
            print(f"Received a message on '{subject}': {self.get_id()}")
            await self.execute()

        def transformer(self, row):
            return row

        def filter_result(self, result):
            return result

        async def process(self):
            row = self.filter_result(self.data)
            transformed = self.transformer(row)
            await self.dispatch(transformed)

        async def execute(self):
            self.fetch()
            await self.process()

        async def worker(self):
            await self.connect()
            await self.subscribe()

            try:
                await self.nc.flush()
            except ErrTimeout:
                print("Flush timeout")

            while True:
                await asyncio.sleep(1)

        async def run(self):
            workers = [deepcopy(self) for _ in range(self.worker_count)]
            await asyncio.gather(*(worker.worker() for worker in workers))

    return Q
