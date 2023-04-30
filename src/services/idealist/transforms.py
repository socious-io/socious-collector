import re
from random import randint
from urllib.parse import urlparse


def get_payment_type(row: dict):
    paid = row.get('paid', None)
    salary_min = row.get('salaryMinimum', 0)
    salary_max = row.get('salaryMaximum', 0)

    if paid or (salary_min and float(salary_min) > 0) or (salary_max and float(salary_max) > 0):
        return 'PAID'

    return 'VOLUNTEER'


def get_remote_preference(row):
    remote = row.get('remoteOk', None)
    remote_tmp = row.get('remoteTemporary', None)

    if remote:
        if remote_tmp:
            return 'HYBRID'

        return 'REMOTE'

    return 'ONSITE'


def get_experience_level(row):
    pr_lev = {
        'NONE': 0,
        'ENTRY_LEVEL': 1,
        'MANAGERIAL': 2,
        'INTERMEDIATE': 2,
        'PROFESSIONAL': 2,
        'DIRECTOR': 3,
        'EXECUTIVE': 3,
        'EXPERT': 3
    }

    level = row.get('professionalLevel', 'NONE')
    return pr_lev.get(level, 0)


def get_org_shortname(row):
    url = row.get('url', {}).get('en', None)

    if url:
        domain = urlparse(url)
        splited = domain.netloc.split('.')
        if len(splited) == 2:
            return splited[0]
        if len(splited) == 3:
            return splited[1]
        return ''.join(splited)

    match = re.search(r'\(?([0-9A-Za-z]+)\)?', row.get('name', ''))
    return '%s%d' % (match.group(1), randint(1000, 9999))


def job_transformer(row: dict) -> dict:
    return {
        'title': row.get('name'),
        'description': row.get('description') or 'No information',
        'remote_preference': get_remote_preference(row),
        'payment_type': get_payment_type(row),
        'payment_scheme': 'HOURLY' if row.get('salaryPeriod') == 'HOUR' else 'FIXED',
        'payment_currency': row.get('salaryCurrency'),
        'payment_range_lower': row.get('salaryMinimum'),
        'payment_range_higher': row.get('salaryMaximum'),
        'experience_level': get_experience_level(row),
        'status': 'ACTIVE',
        'country': row.get('address', {}).get('country'),
        'city': row.get('address', {}).get('city'),
        'other_party_id': row.get('id'),
        'other_party_title': 'IDEALIST',
        'other_party_url': row.get('url', {}).get('en'),
        'updated_at': row.get('updated'),
        'org': org_transform(row.get('org'))
    }


def org_transform(row: dict) -> dict:
    return {
        'name': row.get('name'),
        'bio': ', '.join(row.get('areasOfFocus', [])).lower().replace('_', ''),
        'logo': row.get('logo'),
        'shortname': get_org_shortname(row),
        'type': 'OTHER',
        'address': row.get('address', {}).get('full'),
        'country': row.get('address', {}).get('country'),
        'city': row.get('address', {}).get('city'),
        'other_party_id': row.get('id'),
        'other_party_title': 'IDEALIST',
        'other_party_url': row.get('url', {}).get('en'),
    }
