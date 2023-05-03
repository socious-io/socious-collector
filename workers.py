import asyncio
import importlib
from src.config import config


async def main():
    QUEUES = []
    for service in config.services:
        module = importlib.import_module('src.services.%s' % service)
        if 'QUEUES' not in dir(module):
            continue
        QUEUES += [q.run() for q in module.QUEUES]
        print('%s queues has been start!' % service)

    # Run multiple NATS listeners.
    await asyncio.gather(*QUEUES)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
