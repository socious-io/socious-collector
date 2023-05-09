from .jobs import ReliefwebListingJob, ReliefwebRowQueue

JOBS = (
    ReliefwebListingJob(),
)

QUEUES = (
    ReliefwebRowQueue(),
)
