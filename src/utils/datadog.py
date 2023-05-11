from datadog import initialize, api
from src.config import config

initialize(**config.datadog)


logs = api.Logs
metrics = api.Metric
