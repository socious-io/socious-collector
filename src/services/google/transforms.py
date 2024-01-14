import re
from random import randint
import pycountry


def get_job_type(row: dict):
    data: str = row.get('detected_extensions', {}).get('schedule_type')
    if not data:
        return None
    data = data.lower()
    if 'full' in data:
        return 'FULL_TIME'
    if 'part' in data:
        return 'PART_TIME'
    if 'off' in data:
        return 'ONE_OFF'
    return None


def get_location(location: str):
    splited = location.split(',')
    if len(splited) < 2:
        return None, None

    return splited[0].strip(), pycountry.countries.get(name=splited[1].strip())


def get_org_shortname(row: dict):
    match = re.search(r'\(?([0-9A-Za-z]+)\)?', row.get('company_name', ''))
    return '%s%d' % (match.group(1), randint(1000, 9999))


def job_transformer(row: dict) -> dict:
    country, city = get_location(row.get('location'))
    link = row.get('related_links', [])[0].get('link')
    return {
        'title': row.get('title'),
        'description': row.get('description') or 'No information',
        'status': 'ACTIVE',
        'project_type': get_job_type(row),
        'country': country,
        'city': city,
        'other_party_id': row.get('job_id'),
        'other_party_title': 'GOOGLE',
        'other_party_url': link,
        'org': org_transform(row, country, city, link)
    }


def org_transform(row: dict, country, city, link) -> dict:
    return {
        'name': row.get('company_name'),
        'logo': row.get('thumbnail'),
        'shortname': get_org_shortname(row),
        'type': 'OTHER',
        'address': row.get('location'),
        'country': country,
        'city': city,
        'other_party_id': row.get('id'),
        'other_party_title': 'GOOGLE',
        'other_party_url': link,
    }
