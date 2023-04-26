
def job_transformer(row: dict) -> dict:
    """ const paymentType = await getPaymentType(row)
    const remotePreference = await getRemotePreference(row)

    const experienceLevel = await getExperienceLevel(row) """
    # print(row.get('org'), '&&&&&&&&&&&&&&&&&&&&')
    return {
        'title': row.get('name'),
        'description': row.get('description') or 'No information',
        # remote_preference: remotePreference,
        # payment_type: paymentType,
        'payment_scheme': 'HOURLY' if row.get('salaryPeriod') == 'HOUR' else 'FIXED',
        'payment_currency': row.get('salaryCurrency'),
        'payment_range_lower': row.get('salaryMinimum'),
        'payment_range_higher': row.get('salaryMaximum'),
        # 'experience_level': experienceLevel,
        'status': 'ACTIVE',
        'country': row.get('address', {}).get('country'),
        'city': row.get('address', {}).get('city'),
        'other_party_id': row.get('id'),
        # 'other_party_title': type,
        'other_party_url': row.get('url', {}).get('en'),
        # updated_at: row.updated
    }
