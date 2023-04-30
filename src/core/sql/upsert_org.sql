INSERT INTO organizations (
  name,
  bio,
  shortname,
  type,
  address,
  country,
  city,
  other_party_id,
  other_party_title,
  other_party_url
) VALUES (
  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
ON CONFLICT (other_party_id, other_party_title)
DO UPDATE SET
  id = organizations.id
RETURNING *
