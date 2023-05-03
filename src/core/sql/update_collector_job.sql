UPDATE collector_jobs SET 
  service=%s,
  job_name=%s,
  has_more=%s,
  fetch_counter=%s,
  last_modified_date=%s,
  updated_at=%s
WHERE id=%s
RETURNING *
