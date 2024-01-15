from slugify import slugify


def job_transformer(row: dict) -> dict:
    area = row.get('location', {}).get('area')
    country = None
    city = None
    if len(area) > 1:
        country = area[0]
        city = area[1]

    contract = row.get('contract_time') or 'FULL_TIME'
    if 'part' in contract.lower():
        contract = 'PART_TIME'

    return {
        'title': row.get('title'),
        'project_type': contract,
        'description': row.get('description') or 'No information',
        'payment_scheme': 'FIXED',
        'payment_range_lower': row.get('salary_min'),
        'payment_range_higher': row.get('salary_max'),
        'status': 'ACTIVE',
        'country': country,
        'city': city,
        'other_party_id': row.get('id'),
        'other_party_title': 'ADZUNA',
        'other_party_url': row.get('redirect_url', ''),
        'updated_at': row.get('created'),
        'org': org_transform(row, country, city)
    }


def org_transform(row: dict, country, city) -> dict:
    name = row.get('company', {}).get('display_name', '').strip()
    shortname = slugify(name.strip())
    return {
        'name': name,
        'shortname': shortname,
        'other_party_id': shortname,
        'other_party_title': 'ADZUNA',
        'country': country,
        'city': city
    }
