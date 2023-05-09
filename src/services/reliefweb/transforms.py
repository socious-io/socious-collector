import pycountry


def get_country(row: dict) -> str:
    countries = row.get('country') or []
    if len(countries) < 1:
        return None

    try:
        country = pycountry.countries.get(alpha_3=countries[0].get('iso3'))
        return country.alpha_2
    except Exception:
        return None


def get_city(row: dict) -> str:
    cities = row.get('city') or []
    if len(cities) < 1:
        return None
    return cities[0].get('name')


def get_exp(row: dict) -> int:
    exps = row.get('experience') or []
    if len(exps) < 1:
        return 0

    exp = (exps[0].get('name') or '')

    try:
        years = int(exp.strip()[0])
        if years <= 1:
            return 0
        if years < 2:
            return 1
        if years <= 4:
            return 2
        return 3
    except ValueError:
        return 0


def job_transformer(row: dict) -> dict:
    id = row['id']
    row = row['fields']
    return {
        'title': row.get('title'),
        'description': row.get('body-html') or row.get('body'),
        'country': get_country(row),
        'city': get_city(row),
        'experience_level': get_exp(row),
        'status': 'ACTIVE',
        'other_party_id': id,
        'other_party_title': 'RELIEFWEB',
        'other_party_url': row.get('url'),
        'updated_at': (row.get('date') or {}).get('changed'),
        'org': org_transform(row.get('source')[0])
    }


def org_transform(row: dict) -> dict:
    return {
        'name': row.get('name'),
        'bio': ', '.join(row.get('areasOfFocus') or []).lower().replace('_', ''),
        # 'logo': row.get('logo'),
        'shortname': row.get('shortname'),
        'type': 'OTHER',
        'website': row.get('homepage'),
        'other_party_id': row.get('id'),
        'other_party_title': 'RELIEFWEB',
        'other_party_url': row.get('href'),
    }
