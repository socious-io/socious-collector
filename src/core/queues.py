import asyncio
import json
from copy import deepcopy
from typing import Optional, Any, Dict
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrTimeout
from src.config import config
from src.utils.datadog import push_metric
from src.utils.logger import get_logger

logger = get_logger('queues')

lock = asyncio.Lock()

# Configurable reconnection settings
RECONNECT_DELAY_INITIAL = 1  # seconds
RECONNECT_DELAY_MAX = 60  # seconds


def Queue(Base):

    class Q(Base):
        def __init__(self):
            self.row: Dict[str, Any] = {}
            self.nc = NATS()
            self._reconnect_delay = RECONNECT_DELAY_INITIAL

        @property
        def worker_count(self) -> int:
            return 1

        @property
        def name(self) -> str:
            return 'queue'

        @property
        def subject(self) -> str:
            return 'subject'

        def get_id(self) -> Optional[str]:
            return self.row.get('id')

        def path(self) -> Optional[str]:
            return None

        async def connect(self) -> None:
            if self.nc.is_connected:
                return

            options = {
                "servers": [config.nats_url],
                "connect_timeout": 10,
                "reconnect_time_wait": 2,
                "max_reconnect_attempts": -1,  # Unlimited reconnects
            }
            try:
                await self.nc.connect(**options)
                self._reconnect_delay = RECONNECT_DELAY_INITIAL  # Reset on success
                logger.info(f"Connected to NATS for {self.name}")
            except TimeoutError as e:
                logger.error(f"NATS connection timeout for {self.name}: {e}")
                await self._handle_reconnect()
            except Exception as e:
                logger.error(f"NATS connection error for {self.name}: {e}")
                await self._handle_reconnect()

        async def _handle_reconnect(self) -> None:
            """Handle reconnection with exponential backoff."""
            logger.warning(f"Reconnecting to NATS in {self._reconnect_delay}s...")
            await asyncio.sleep(self._reconnect_delay)
            # Exponential backoff with max limit
            self._reconnect_delay = min(self._reconnect_delay * 2, RECONNECT_DELAY_MAX)
            await self.connect()

        async def subscribe(self) -> None:
            await self.nc.subscribe(self.subject, queue=self.name, cb=self.handler)
            logger.info(f"Subscribed to {self.subject} on queue {self.name}")

        async def dispatch(self, data: Dict[str, Any]) -> None:
            if (self.queue):
                await self.queue.publish(data)

        async def publish(self, row: Dict[str, Any]) -> None:
            await self.connect()
            await self.nc.publish(self.subject, json.dumps(row).encode())

        async def handler(self, msg) -> None:
            subject = msg.subject
            self.row = json.loads(msg.data.decode())
            push_metric(self.subject, 1)
            logger.debug(f"Received message on '{subject}': {self.get_id()}")
            await self.execute()

        def transformer(self, row: Dict[str, Any]) -> Dict[str, Any]:
            return row

        def filter_result(self, result: Any) -> Any:
            return result

        async def process(self) -> None:
            row = self.filter_result(self.data)
            transformed = self.transformer(row)
            await self.dispatch(transformed)

        async def execute(self) -> None:
            try:
                self.fetch()
                await self.process()
            except Exception as err:
                logger.error(f"Error executing queue {self.name}: {err}")

        async def worker(self) -> None:
            await self.connect()
            await self.subscribe()

            try:
                await self.nc.flush()
            except ErrTimeout:
                logger.warning(f"Flush timeout for {self.name}")

            while True:
                await asyncio.sleep(1)

        async def run(self):
            workers = [deepcopy(self) for _ in range(self.worker_count)]
            await asyncio.gather(*(worker.worker() for worker in workers))

    return Q
