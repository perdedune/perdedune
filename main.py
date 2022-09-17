from sql_from_dashboard import query_list, sql_from_query, sql_extractor

# enter dashboard url here
dashboard_url = "https://dune.com/perdedune/perdedune"

# extract unique sql files from dashboard
sql_extractor(dashboard_url)

