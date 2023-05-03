INSERT INTO collector_jobs (
  service,
  job_name,  
  has_more,
  fetch_counter,
  last_modified_date,
  updated_at
) VALUES (%s, %s, %s, %s, %s, %s)
RETURNING *
