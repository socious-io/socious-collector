from src.core.worker import Worker


class ListingWorker(Worker(object)):
    @property
    def name(self):
        return 'listings'

    @property
    def subject(self):
        return 'listings'

    async def execute(self):
        print(self.row)
