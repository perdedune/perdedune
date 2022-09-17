SELECT "rank_number",
          CONCAT('<a href="https://blockscout.com/xdai/mainnet/address/',replace("address"::text, '\', '0'),'" target="_blank" >',replace("address"::text, '\', '0'),'</a>') as "address",
          "balance",
          "perc",
          sum("perc") over (order by rank_number asc rows between unbounded preceding and current row) as "cumulative_perc"
        --   COUNT(*) OVER () as "total_holders",
        --   SUM("balance") OVER () as "supply"
FROM abstraction_0

