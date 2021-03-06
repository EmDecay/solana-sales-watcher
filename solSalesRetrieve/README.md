# solSalesRetrieve
This is the code that queries and stores recent sales in a SQLite database.  Update `auth_address` to point to the CMID of the candy machine that minted the NFT's (look for the 0% royalty wallet).  This code is currently intended to be run as either a cron job or manually in the terminal, and the error handling needs some improvement.  I plan to move this from a cron job to the loop method used by the Tweet code in a future iteration, but for now this works.  There are several variables towards the top of the file (`debug`, `showall`, `verbose`) that control how verbose the output is.  When running as a cron job, it's best to set these all to false.

Yes, the code is multi-threaded and you can lookup a significant number of transactions very quickly.  Currently, it only can go back up to 1,000 transactions (I have not yet added pagination code to go further back).  I have hit many-an-RPS limit with this threading code; be aware that setting this too high may make the RPC API endpoint you are using "not happy with you."

For usage, try:

`solsaleswatch.py --help`