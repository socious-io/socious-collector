from .jobs import IdealistListingJob, IdealistRowQueue

JOBS = (
    IdealistListingJob('jobs'),
    # IdealistListingJob('volops'),
    # IdealistListingJob('internships'),
)

QUEUES = (
    IdealistRowQueue('jobs'),
    # IdealistRowQueue('volops'),
    # IdealistRowQueue('internships'),
)
