import pycountry


themes_to_social_cause = {
    '4587': 'HUNGER',
    '49458': 'SUSTAINABLE_COMMUNITIES',
    '4588': 'CLIMATE_CHANGE',
    '4590': 'COLLABORATION_FOR_IMPACT',
    '4591': 'NATURAL_DISASTERS',
    '4592': 'EDUCATION',
    '4593': 'HUNGER',
    '4594': 'GENDER_EQUALITY',
    '4595': 'HEALTH',
    '4596': 'HEALTH',
    '12033': 'PEACE_JUSTICE',
    '4599': 'PEACEBUILDING',
    '4600': 'HUMAN_RIGHTS',
    '4601': 'SUSTAINABLE_COMMUNITIES',
    '4602': 'SECURITY',
    '4603': 'SUSTAINABLE_COMMUNITIES',
    '4604': 'WATER_SANITATION'

}


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


def get_causes(row: dict):
    causes = []
    themes = row.get('theme') or []

    for theme in themes:
        cause = themes_to_social_cause.get(str(theme.get('id')))
        if cause is not None and cause not in causes:
            causes.append(cause)

    return causes


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
        'org': org_transform(row.get('source')[0]),
        'causes_tags': get_causes(row)
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
