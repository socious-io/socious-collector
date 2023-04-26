import asyncio
import json
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrTimeout
from src.config import config


def Worker(Base):

    class Q(Base):
        def __init__(self):
            self.row = {}
            self.nc = NATS()

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
            options = {
                "servers": [config.nats_url],
            }
            await self.nc.connect(**options)

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
            print(f"Received a message on '{subject}': {self.row}")
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

        async def run(self):
            await self.connect()
            await self.subscribe()

            try:
                await self.nc.flush()
            except ErrTimeout:
                print("Flush timeout")

            while True:
                await asyncio.sleep(1)
    return Q
