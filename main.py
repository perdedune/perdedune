import argparse

from sql_from_dashboard import sql_extractor

parser = argparse.ArgumentParser(
    usage="%(prog)s [OPTION] [URL]...",
    description="Pull all SQL from a Dune Dashboard URL",
)
parser.add_argument("url", nargs=1) #"https://dune.com/perdedune/perdedune"
args = parser.parse_args()

# extract unique sql files from dashboard
sql_extractor(args.url[0])
