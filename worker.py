import asyncio
from src.services.idealist.jobs import IdealistRowQueue


worker = IdealistRowQueue()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(worker.run())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
