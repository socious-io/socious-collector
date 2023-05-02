from src.core.queues import Queue
from src.core.models.jobs import JobsEntity
from src.core.models.organizations import OrganizationEntity
from src.core.models.media import MediaEntity


class ListingWorker(Queue(object)):
    @property
    def name(self):
        return 'listings'

    @property
    def subject(self):
        return 'listings'

    def get_id(self):
        return self.row.get('other_party_id')

    async def execute(self):
        org = self.row.get('org')
        logo = org.get('logo')
        org_entity = OrganizationEntity(org)
        org_entity.sync()
        if logo:
            MediaEntity({
                'identity_id': org_entity.get_id(),
                'filename': 'logo',
                'url': logo
            }).sync()

        self.row['identity_id'] = org_entity.get_id()
        job_entity = JobsEntity(self.row)
        job_entity.sync()
