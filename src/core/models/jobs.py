from . import BaseEntity


class JobsEntity(BaseEntity):

    @property
    def fetch_query_name(self):
        return 'get_job'

    @property
    def fetch_query_params(self):
        return (self.row['other_party_id'],
                self.row['other_party_title'])

    @property
    def sync_query_name(self):
        return 'upsert_job'

    @property
    def columns(self) -> tuple:
        return (
            'id',
            'identity_id',
            'title',
            'description',
            'remote_preference',
            'payment_type',
            'payment_scheme',
            'payment_currency',
            'payment_range_lower',
            'payment_range_upper',
            'experience_level',
            'status',
            'country',
            'city',
            'other_party_id',
            'other_party_title',
            'other_party_url',
            'updated_at',
            'impact_job'
        )
