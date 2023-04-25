def ListingsJob(Base):

    class Job(Base):

        @property
        def job_name(self):
            return '%s.listings_job' % self.name

        def filter_result(self, result):
            return result

        def pre_process(self, row):
            return row

        def transformer(self, row):
            return row

        def process(self):
            for row in self.rows:
                row = self.pre_process(row)
                transformed = self.transformer(row)
                self.dispatch(self.job_name, transformed)

        def execute(self):
            self.fetch()
            self.process()

    return Job
