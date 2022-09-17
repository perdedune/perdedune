SELECT  COUNT(*) OVER () as "total_holders",
        SUM("balance") OVER () as "supply"
FROM abstraction_0

