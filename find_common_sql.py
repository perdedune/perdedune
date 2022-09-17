import difflib
import argparse
from os import path

from pprint import pp
from pglast import parse_sql
from pglast.parser import parse_sql_json
from pglast.stream import RawStream, IndentedStream
from pathlib import Path

def deepp(h, depth=5):
	pp(h.stmt(depth=depth, skip_none=True))

# parse args
parser = argparse.ArgumentParser(
	usage="%(prog)s [OPTION] [FILE]...",
	description="prettify SQL statements and check for similar clauses",
)
parser.add_argument(
	"-v", "--version", action="version",
	version=f"{parser.prog} version 1.0.0"
)
parser.add_argument("files", nargs="*")
args = parser.parse_args()

# extract filenames
filenames = []
filenames.append(os.path.basename(args.files[0]).split('.')[0])
filenames.append(os.path.basename(args.files[1]).split('.')[0])

print("filenames", filenames)

# open both files
with open(args.files[0]) as f:
	holders = f.read()
with open(args.files[1]) as g:
	marketinfo = g.read()

h = parse_sql(holders)[0]
m = parse_sql(marketinfo)[0]
print("Will **** be successfully sucked:", h.stmt.withClause == m.stmt.withClause) # true

h_prettyprinted = IndentedStream()(h)
m_prettyprinted = IndentedStream()(m)

s = difflib.SequenceMatcher(None, h_prettyprinted, m_prettyprinted)
match = s.find_longest_match()
if match.size > 0:
	print("Found similar SQL, writing to abstraction.sql")
else:
	print("Couldn't find similar SQL, aborting")
	exit()
Path("output").mkdir(parents=True, exist_ok=True)
with open('output/abstraction.sql', 'w') as f:
	f.write(h_prettyprinted[match.a:match.size])

print("writing the different part to difference files")
with open('output/{}.sql'.format(filenames[0]), 'w') as f:
	f.write("SELECT " + h_prettyprinted[match.size:])
with open('output/{}.sql'.format(filenames[1]), 'w') as f:
	f.write("SELECT " + m_prettyprinted[match.size:])
