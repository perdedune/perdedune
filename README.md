# Perdedune
Automagically parse queries from a dashboard to remove duplicate sets and streamline your code!

### perdedune tool demo
[![asciicast](https://asciinema.org/a/uOOS9DwAKtDTud4QmJyCpfD84.svg)](https://asciinema.org/a/uOOS9DwAKtDTud4QmJyCpfD84)

## Usage:
Run the following commands in your terminal:
```
git clone https://github.com/perdedune/perdedune/ ./perdedune
cd perdedune
pip install -r requirements.txt

python main.py "https://dune.com/perdedune/perdedune"
# new directory perdedune_perdedune was created

python find_common_sql.py perdedune_perdedune
# abstractions(common sql statements) and unique select statements written to perdedune_perdedune/output
```

## Output:
* main.py will extract a number of user_dashboard/input/*.sql files, representing the existing SQL logic for all queries in the dashboard.
* find_common_sql.py analyses the sql files generated by main.py, and outputs a more optimal solution under user_dashboard/output/*.sql. 

## Architecture:

<img src=diagram.jpg>

## Sample data
In order to validate our process, we sampled an existing Dune table using the Dune API.
The script and sample data are available at /sample_data.
To re-extract, simply run /sample_data/sample_data.py.

## Known limitations:
* At the moment, the process is limited to CTE, and  queries.
* Further, the process currently assumes a unique CTE alias scheme.
