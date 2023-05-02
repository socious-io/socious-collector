from .listings import ListingWorker

QUEUES = [
    ListingWorker()
]
