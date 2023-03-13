from google.cloud import bigquery
from time import time

client = bigquery.Client()


def show_amount_of_data_scanned(query):
    # dry_run let us see how much datathe query uses without running it
    dry_run_conf = bigquery.QueryJobConfig(dry_run_conf=True)
    query_job = client.query(query, job_config=dry_run_conf)
    print('Data processed: %s GB' % (round(query_job.total_bytes_processed / 10**9, 3)))


def show_time_to_run(query):
    time_config = bigquery.QueryJobConfig(use_query_cache=False)
    start = time()
    query_result = client.query(query, job_config=time_config).result()
    end = time()
    print('Time to run: %s seconds' % round(end-start, 3))