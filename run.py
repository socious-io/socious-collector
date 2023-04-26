import asyncio
from src.services.idealist.jobs import IdealistListingJob


job = IdealistListingJob()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(job.execute())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()