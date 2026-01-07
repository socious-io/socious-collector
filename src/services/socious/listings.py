import json
from psycopg2.extras import Json
from src.core.queues import Queue
from src.config import config
from src.core.db import DB
from src.core.models.jobs import JobsEntity
from src.core.models.organizations import OrganizationEntity
from src.core.models.media import MediaEntity
from src.utils.datadog import push_metric
from src.utils.http import async_post
from src.utils.logger import get_logger

logger = get_logger('socious_listings')


class ListingWorker(Queue(object)):
    @property
    def name(self):
        return 'SOCIOUS.listings'

    @property
    def subject(self):
        return 'SOCIOUS.listings'

    def get_id(self):
        return self.row.get('other_party_id')

    async def is_job_impact(self) -> bool:
        """Check if job is impact-related using async HTTP client."""
        if self.row['other_party_title'] in ['IDEALIST', 'RELIEFWEB']:
            return True

        try:
            json_data = {
                'query': [{'title': self.row.get('title'), 'description': self.row.get('title')}]
            }
            url = config.impact_job_detector.get('url')
            if not url:
                logger.warning("Impact job detector URL not configured")
                return False

            res = await async_post(url, json_data=json_data)
            return bool(res.get('predicts', [])[0]) if res.get('predicts') else False
        except Exception as err:
            logger.error(f'Impact job detector error: {err}')
            return False

    async def is_org_impact(self) -> bool:
        """Check if organization is impact-related using async HTTP client."""
        if self.row['other_party_title'] in ['IDEALIST', 'RELIEFWEB']:
            return True

        try:
            json_data = {
                'query': [{'name': self.row.get('org').get('title'), 'description': self.row.get('org').get('description')}]
            }
            url = config.impact_org_detector.get('url')
            if not url:
                logger.warning("Impact org detector URL not configured")
                return False

            res = await async_post(url, json_data=json_data)
            return bool(res.get('predicts', [])[0]) if res.get('predicts') else False
        except Exception as err:
            logger.error(f'Impact org detector error: {err}')
            return False

    async def execute(self):
        org_only = self.row.get('org_only')
        org = self.row.get('org')
        org['impact_detected'] = await self.is_org_impact()
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
        if org_only:
            logger.info(f'Organization {org_entity.get_id()} synced (org only)')
            return
        tags = self.row.get('causes_tags')
        if tags and len(tags) > 0:
            self.row['causes_tags'] = '{' + \
                ",".join([f'{tag}' for tag in tags]) + '}'
        self.row['impact_job'] = await self.is_job_impact()
        self.row['identity_id'] = org_entity.get_id()
        job_entity = JobsEntity(self.row)
        if job_entity.fetch():
            logger.debug(f'{job_entity.get_id()} already synced')
            return
        job_entity.sync()
        logger.info(f'Job {job_entity.get_id()} synced')
        push_metric('job_synced', 1)
