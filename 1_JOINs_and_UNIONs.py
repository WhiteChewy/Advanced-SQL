from google.cloud import bigquery

client = bigquery.Client()
dataset_ref = client.dataset('hacker_news', project='bigquery-public-data')
dataset = client.get_dataset(dataset_ref)
table_ref = dataset_ref.table('comments')
table = client.get_table(table_ref)
client.list_rows(table, max_results=5).to_dataframe()

another_table_ref = dataset_ref.table('stories')
another_table = client.get_table(table_ref)
client.list_rows(table, max_results=5).to_dataframe()


join_query = """
             WITH c AS
             (
                SELECT parent, COUNT(*) as num_comments
                FROM `bigquery-public-data.hacker_news.comments`
                GROUP BY parent
             )
             SELECT s.id as stroy_id, s.by, s.tittle, c.num_comments
             FROM `bigquery-public-data.hacker_news.stories` AS s
             LEFT JOIN c
             ON s.id = c.parent
             WHERE EXTRACT(DATE FROM s.time_ts) = '2012-01-01'
             ORDER BY c.num_comments DESC
             """
join_result = client.query(join_query).result().to_dataframe()
join_result.head()
join_result.tail()

union_query = """
              SELECT c.by
              FROM `bigquery-public-data.hacker_news.comments` AS c
              WHERE EXTRACT(DATE FROM c.time_ts) = '2014-01-01'
              UNION DISTINCT
              SELECT s.by
              FROM `bigquery-public-data.hacker_news.stories` AS s
              WHERE EXTRACT(DATE FROM s.time_ts) = '2014-01-01'
              """

union_result = client.query(union_query).result().to_dataframe()
union_result.head()
print(len(union_result))
