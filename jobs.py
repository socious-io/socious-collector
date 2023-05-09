import asyncio
import importlib
from src.config import config


async def main():
    JOBS = []
    for service in config.services:
        module = importlib.import_module('src.services.%s' % service)
        if 'JOBS' not in dir(module):
            continue
        JOBS += [j.run() for j in module.JOBS]
        print('%s job has been start!' % service)

    await asyncio.gather(*JOBS)


if __name__ == "__main__":
    try:
      asyncio.run(main())
    except KeyboardInterrupt:
      pass
    finally:
      loop = asyncio.get_event_loop()
      loop.close()
