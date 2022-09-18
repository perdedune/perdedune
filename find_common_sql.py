import difflib
import argparse
from os import path

from pprint import pp
from pathlib import Path
from os import path
from collections import namedtuple
import sqlglot

def deepp(h, depth=5):
	pp(h.stmt(depth=depth, skip_none=True))

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


Sql = namedtuple('Sql', ['parsed', 'filename'])
Abstraction = namedtuple('Abstraction', ['sql', 'alias'])
sqls = []
for file in args.files:
	with open(file) as x:
		sql = Sql(x.read(), path.basename(file))
		sqls.append(sql)

asts = [sqlglot.parse_one(sql.parsed) for sql in sqls]

ctes = []
for a in asts:
	ctes.extend(a.ctes)
print(len(ctes), "CTEs found,", len(set(ctes)), "of which are unique")
ctes = list(set(ctes))

abstractions = []
for cte in ctes:
	# transform WITH( SELECT * FROM FDSA ) -> SELECT * FROM FDSA
	with_stmt_removed = [f for f in cte.flatten()][0]
	abstractions.append(Abstraction(with_stmt_removed.sql(pretty=True), cte.alias))


for a in abstractions:
	with open("output/{}.sql".format(a.alias), "w") as f:
		f.write(a.sql)
