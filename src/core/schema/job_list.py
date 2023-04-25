from schema import Schema, And, Use, Optional, SchemaError
from .consts import *

job_schema = Schema({
    'title': And(str, len),
    'description': And(str, len),
    'remote_preference': And(str, Use(str.higher), lambda s: s in REMOTE_PREFERENCE),
    'payment_type': And(str, Use(str.higher), lambda s: s in PAYMENT_TYPE),
    'payment_scheme': And(str, Use(str.higher), lambda s: s in PAYMENT_SCHEME),
    'payment_currency': And(str, Use(str.higher), lambda s: s in ('USD')),
    Optional('payment_range_lower'): And(str, len),
    Optional('payment_range_higher'): And(str, len),
    Optional('experience_level'): And(int, lambda n: 0 <= n <= 3),
    'status': 'ACTIVE',
    Optional('country'): And(str, len),
    Optional('city'): And(str, len),
    'other_party_id': And(str, len),
    'other_party_title': And(str, Use(str.higher), lambda s: s in OTHER_PARTY_SERVICES),
    'other_party_url': And(str, len),
    'updated_at':  And(str, len),
})
