# dbinit.py - Initialize the database connectivity for solSalesWatch
# Author - Matt (emdecay (at) protonmail.com)

import os, sqlite3

db = "solsaleswatch.db"

# If database doesn't yet exist, initialize it with the table structure
def dbinit():
    if not os.path.isfile(db):
        print ("No database found; initializing \'" + db + "\'...")
        # Initialize database
        dbconn = sqlite3.connect(db)
        dbc = dbconn.cursor()
        dbc.execute("CREATE TABLE tx(name TEXT, collection TEXT, description TEXT, imageurl TEXT, cost FLOAT, txid TEXT)")
        dbconn.commit()
        dbconn.close()