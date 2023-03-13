from google.cloud import bigquery

client = bigquery.Client()
dataset_ref = client.dataset('google_analytics_sqmple', project='bigquery-public-data')
table_ref = dataset_ref.table('ga_sessions_20170801')
dataset = client.get_dataset(dataset_ref)
table = client.get_table(table_ref)
client.list_rows(table, max_results=5).to_dataframe()

print("SCHEMA field for the 'totals' column:\n")
print(table.schema[5])

print("\nSCHEMA field for the 'device' column:\n")
print(table.schema[7])

# Query to count the number of transactions per browser
query = """
        SELECT device.browser AS device_browser,
            SUM(totals.transactions) as total_transactions
        FROM `bigquery-public-data.google_analytics_sample.ga_sessions_20170801`
        FROUP BY device_browser
        ORDER BY total_transactions DESC
        """

result = client.query(query).result().to_dataframe()
print(result.head())

# Query to determine most popular landing point on the website
query = """
        SELECT hits.page.pagePath as path,
            COUNT(hits.page.pagePath) as counts
        FROM `bigquery-public-data.google_analytics_sample.ga_sessions_20170801`,
            UNNEST(hits) as hits
        WHERE hits.type='PAGE' and hits.hitNumber=1
        GROUP BY path
        ORDER BY counts DESC
        """

result = client.query(query).result().to_dataframe()
print(result.head())



