import dotenv
import os
import pandas as pd
#import csv

# this extracts the sample we need to query against within postgres against as a csv.
query_id_= 1278746
name_='erc20.ERC20_evt_Transfer'

from dune_client.types import QueryParameter
from dune_client.client import DuneClient
from dune_client.query import Query


if __name__ == "__main__":
    query = Query(
        name=name_,
        query_id=query_id_,
    )
    dotenv.load_dotenv()
    dune = DuneClient(os.environ["DUNE_API_KEY"])
    query_res = dune.refresh(query)

    df = pd.DataFrame(query_res)
    df.to_csv('./sample_data/{}.csv'.format(name_), index = None)