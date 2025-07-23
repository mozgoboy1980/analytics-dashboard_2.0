from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric
from google.oauth2 import service_account
from config.settings import GA4_PROPERTY_ID, START_DATE, END_DATE, SERVICE_ACCOUNT_FILE

def fetch_ga4_data():
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
    client = BetaAnalyticsDataClient(credentials=credentials)

    request = RunReportRequest(
        property=f"properties/{GA4_PROPERTY_ID}",
        dimensions=[Dimension(name="pageTitle"), Dimension(name="pagePath")],
        metrics=[Metric(name="activeUsers"), Metric(name="engagementRate")],
        date_ranges=[DateRange(start_date=START_DATE, end_date=END_DATE)]
    )

    response = client.run_report(request)
    rows = [[dim.value for dim in row.dimension_values] +
            [metric.value for metric in row.metric_values] for row in response.rows]
    return rows
