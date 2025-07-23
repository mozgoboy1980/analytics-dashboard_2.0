from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric
from google.oauth2 import service_account
from config.settings import GA4_PROPERTY_ID, SERVICE_ACCOUNT_FILE

def fetch_ga4_data(start_date: str, end_date: str, metric_names: list):
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
    client = BetaAnalyticsDataClient(credentials=credentials)

    dimensions = [Dimension(name="pageTitle"), Dimension(name="pagePath")]
    metrics = [Metric(name=m) for m in metric_names]

    request = RunReportRequest(
        property=f"properties/{GA4_PROPERTY_ID}",
        dimensions=dimensions,
        metrics=metrics,
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)]
    )

    response = client.run_report(request)
    rows = [[dim.value for dim in row.dimension_values] +
            [metric.value for metric in row.metric_values] for row in response.rows]
    return rows
