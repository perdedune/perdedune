# Perdedune
Automagically parse queries from a dashboard to remove duplicate sets and streamline your code!

<img src=img/1.jpeg/>

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

## Architecture:


## Known limitations:
* At the moment, the process is limited to CTE, and  queries.
* Further, the process currently assumes a unique CTE alias scheme.
