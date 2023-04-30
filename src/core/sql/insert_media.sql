INSERT INTO media 
  (identity_id, filename, url)
VALUES (%s, %s, %s)
RETURNING *
