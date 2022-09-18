from sql_from_dashboard import sql_extractor
import argparse

args = parser.parse_args()
# enter dashboard url here
dashboard_url = args.files[0] #"https://dune.com/perdedune/perdedune"

# extract unique sql files from dashboard
sql_extractor(dashboard_url)

