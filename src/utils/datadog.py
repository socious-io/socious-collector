from datetime import datetime
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.metrics_api import MetricsApi
from datadog_api_client.v2.model.metric_intake_type import MetricIntakeType
from datadog_api_client.v2.model.metric_payload import MetricPayload
from datadog_api_client.v2.model.metric_point import MetricPoint
from datadog_api_client.v2.model.metric_series import MetricSeries


configuration = Configuration()
api_client = ApiClient(configuration)


def push_metric(name, points):
    try:
        body = MetricPayload(
            series=[
                MetricSeries(
                    metric=name,
                    type=MetricIntakeType.UNSPECIFIED,
                    points=[
                        MetricPoint(
                            timestamp=int(datetime.now().timestamp()),
                            value=points,
                        ),
                    ],
                ),
            ],
        )
        api_instance = MetricsApi(api_client)
        response = api_instance.submit_metrics(body=body)
        errors = response.get('errors')
        if len(errors) > 0:
            print('datadog metric submit errors : %s' % errors)
    except Exception as err:
        print(err)
