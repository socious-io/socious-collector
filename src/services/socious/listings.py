from src.core.queues import Queue
from src.core.db import DB
from src.core.models.jobs import JobsEntity
from src.core.models.organizations import OrganizationEntity
from src.core.models.media import MediaEntity
from src.utils.datadog import push_metric


class ListingWorker(Queue(object)):
    @property
    def name(self):
        return 'SOCIOUS.listings'

    @property
    def subject(self):
        return 'SOCIOUS.listings'

    def get_id(self):
        return self.row.get('other_party_id')

    async def execute(self):
        org = self.row.get('org')
        logo = org.get('logo')
        org_entity = OrganizationEntity(org)
        org_entity.sync()
        if logo:
            media = MediaEntity({
                'identity_id': org_entity.get_id(),
                'filename': 'logo',
                'url': logo
            })
            media.sync()
            DB.query('update_org_media',
                     (media.row['id'], org_entity.get_id()))

        self.row['identity_id'] = org_entity.get_id()
        job_entity = JobsEntity(self.row)
        if job_entity.fetch():
            return
        job_entity.sync()
        print('%s has been synced' % job_entity.get_id())
        push_metric('job_synced', 1)
