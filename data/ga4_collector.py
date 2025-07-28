import os
import json
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Metric
from google.oauth2 import service_account
from config.settings import GA4_PROPERTY_ID

def fetch_total_ga4_data(start_date: str, end_date: str, metric_names: list):
    key_data = json.loads(os.environ["GA4_KEY_JSON"])
    credentials = service_account.Credentials.from_service_account_info(key_data)

    client = BetaAnalyticsDataClient(credentials=credentials)
    metrics = [Metric(name=m) for m in metric_names]

    request = RunReportRequest(
        property=f"properties/{GA4_PROPERTY_ID}",
        metrics=metrics,
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)]
    )

    response = client.run_report(request)
    result_row = [value.value for value in response.rows[0].metric_values]
    return result_row
