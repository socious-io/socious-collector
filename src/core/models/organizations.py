from . import BaseEntity


class OrganizationEntity(BaseEntity):

    @property
    def fetch_query_name(self):
        return 'get_org'

    @property
    def fetch_query_params(self):
        return (self.row['other_party_id'],
                self.row['other_party_title'])

    @property
    def sync_query_name(self):
        return 'upsert_org'

    @property
    def columns(self) -> tuple:
        return (
            'id',
            'name',
            'bio',
            'shortname',
            'type',
            'address',
            'country',
            'city',
            'website',
            'other_party_id',
            'other_party_title',
            'other_party_url',
        )
