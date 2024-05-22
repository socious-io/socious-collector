import re
from random import randint
import pycountry


def get_location(identifiers):
    city = None
    country = None

    for id in identifiers:
        loc_type = id.get('location_type')
        if loc_type == 'city' and city is None:
            city = id.get('value')
        if loc_type == 'region':
            city = id.get('value')
        if loc_type == 'country':
            try:
                country = pycountry.countries.get(name=id.get('value')).alpha_2
            except:
                pass

    return country, city


def job_transformer(row: dict) -> dict:
    return {
        'org_only': True,
        'other_party_id': row.get('uuid'),
        'other_party_title': 'CRUNCHBASE',
        'other_party_url': row.get('website_url'),
        'org': org_transform(row),
    }


def org_transform(row: dict) -> dict:
    id = row.get('uuid')
    row = row.get('properties')
    country, city = get_location(row.get('location_identifiers'))
    return {
        'name': row.get('name'),
        'logo': row.get('image_url'),
        'shortname': row.get('identifier').get('permalink'),
        'type': 'OTHER',
        'country': country,
        'description': row.get('short_description'),
        'city': city,
        'other_party_id': id,
        'other_party_title': 'CRUNCHBASE',
        'other_party_url': row.get('website_url'),
        'website': row.get('website_url'),
    }
