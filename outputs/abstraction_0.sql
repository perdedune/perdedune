WITH transfers AS (
    SELECT
    evt_tx_hash AS tx_hash,
    tr."from" AS address,
    -tr.value AS amount,
    contract_address
     FROM erc20."ERC20_evt_Transfer" tr
     WHERE contract_address = '\x5dF8339c5E282ee48c0c7cE8A7d01a73D38B3B27'
UNION ALL
    SELECT
    evt_tx_hash AS tx_hash,
    tr."to" AS address,
    tr.value AS amount,
      contract_address
     FROM erc20."ERC20_evt_Transfer" tr 
     WHERE contract_address = '\x5dF8339c5E282ee48c0c7cE8A7d01a73D38B3B27'
),
transferAmounts AS (
    SELECT address,
            sum(amount)/1e18 as balance
    FROM transfers 
    GROUP BY 1
    ORDER BY 2 DESC
),


getRankingAndPercentage as (
SELECT *,"balance"/SUM("balance") OVER () as "perc" FROM (
    SELECT DISTINCT RANK () OVER ( 
          ORDER BY balance desc
    	) rank_number,CONCAT('0x',(encode("address",'hex'))) as "address",
           "balance"
    FROM transferAmounts
    WHERE balance > 0
    ) x
)

select * from getRankingAndPercentage