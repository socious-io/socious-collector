INSERT INTO organizations (
  name,
  bio,
  shortname,
  type,
  address,
  country,
  city,
  website,
  other_party_id,
  other_party_title,
  other_party_url,
  description,
  impact_detected
) VALUES (
  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
ON CONFLICT (other_party_id, other_party_title)
DO UPDATE SET
  id = organizations.id
RETURNING *
