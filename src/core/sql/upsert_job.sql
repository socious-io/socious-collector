INSERT INTO projects (
  identity_id,
  title,
  description,
  remote_preference,
  payment_type,
  payment_scheme,
  payment_currency,
  payment_range_lower,
  payment_range_higher,
  experience_level,
  status,
  country,
  city,
  other_party_id,
  other_party_title,
  other_party_url,
  updated_at,
  impact_job
) VALUES (
  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
ON CONFLICT ON CONSTRAINT projects_other_party_id_other_party_title_key
DO UPDATE SET
  identity_id=COALESCE(EXCLUDED.identity_id, projects.identity_id),
  title=COALESCE(EXCLUDED.title, projects.title),
  description=COALESCE(EXCLUDED.description, projects.description),
  remote_preference=COALESCE(EXCLUDED.remote_preference, projects.remote_preference),
  payment_type=COALESCE(EXCLUDED.payment_type, projects.payment_type),
  payment_scheme=COALESCE(EXCLUDED.payment_scheme, projects.payment_scheme),
  payment_currency=COALESCE(EXCLUDED.payment_currency, projects.payment_currency),
  payment_range_lower=COALESCE(EXCLUDED.payment_range_lower, projects.payment_range_lower),
  payment_range_higher=COALESCE(EXCLUDED.payment_range_higher, projects.payment_range_higher),
  experience_level=COALESCE(EXCLUDED.experience_level, projects.experience_level),
  status=COALESCE(EXCLUDED.status, projects.status),
  country=COALESCE(EXCLUDED.country, projects.country),
  city=COALESCE(EXCLUDED.city, projects.city),
  other_party_url=COALESCE(EXCLUDED.other_party_url, projects.other_party_url),
  updated_at=COALESCE(EXCLUDED.updated_at, NOW()),
  impact_job=EXCLUDED.impact_job

RETURNING *
