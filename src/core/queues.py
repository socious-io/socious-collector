def Queue(Base):

    class Q(Base):

        def __init__(self, job, row):
            self.row = row
            self.listings_job = job

        @property
        def id(self):
            return self.row.get('id')

        @property
        def path(self):
            return '%s/%s' % (self.listings_job.path, self.id)

        def transformer(self, row):
            return row

        def process(self):
            transformed = self.transformer(self.row)
            self.dispatch(self.job_name, transformed)

        def execute(self):
            self.fetch()
            self.process()

    return Q
