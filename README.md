# EveryPay Payment Gateway Optimization
EveryPay uses several acquiring banks to process their millions of e-commerce transactions. Different acquiring banks have vastly different fail rates for different credit card BIN numbers. This script optimizes which transactions to send to which banks based on the underlying credit card's BIN number.

Notably, the script requires a minimum threshold of 30 transactions for it to provide a fail rate. This ensures that small sample size variance doesn't determine thousands future transactions.

Once run, this script outputs a CSV file that showcases the fail rates (if calculated) for the different banks. This script (and sheet) are used to route future transactions to optimize the transaction success rate.
