import argparse
import difflib
import glob
from collections import namedtuple
from os import path
from pathlib import Path

import sqlglot


def deepp(h, depth=5):
	pp(h.stmt(depth=depth, skip_none=True))

parser = argparse.ArgumentParser(
	usage="%(prog)s PROJECT...",
	description="prettify SQL statements and check for similar clauses",
)
parser.add_argument("project", type=str)
args = parser.parse_args()

# find project_name/input/*.sql files
files = glob.glob("{}/input/*.sql".format(args.project))

Sql = namedtuple('Sql', ['parsed', 'filename'])
Abstraction = namedtuple('Abstraction', ['sql', 'alias'])

sqls = []
for file in files:
	with open(file) as x:
		sql = Sql(sqlglot.parse_one(x.read()), path.basename(file))
		sqls.append(sql)

# sqls = [sqlglot.parse_one(sql.parsed) for sql in sqls]

ctes = []
for sql in sqls:
	ctes.extend(sql.parsed.ctes)
print(len(ctes), "CTEs found,", len(set(ctes)), "of which are unique")
ctes = list(set(ctes))

abstractions = []
for cte in ctes:
	# transform WITH( SELECT * FROM FDSA ) -> SELECT * FROM FDSA
	with_stmt_removed = [f for f in cte.flatten()][0]
	abstractions.append(Abstraction(with_stmt_removed.sql(pretty=True), cte.alias))
# write out the abstractions
Path("{}/output".format(args.project)).mkdir(parents=True, exist_ok=True)
for a in abstractions:
	with open("{}/output/{}.sql".format(args.project, a.alias), "w") as f:
		f.write(a.sql)

# write the last unique sql queries
for sql in sqls:
	# remove the WITH CTE, reconstruct the remaining SELECT statement
	flattened = [x for x in sql.parsed.flatten()]
	flattened = flattened[:len(flattened)-1] # removes the WITH CTE
	answer = sqlglot.expressions.select(*flattened)

	# write to file
	with open("{}/output/{}".format(args.project, sql.filename), "w") as f:
		f.write(answer.sql(pretty=True))
