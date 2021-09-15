# dbinit.py - Initialize the database connectivity for solSalesWatch
# Author - Matt (emdecay (at) protonmail.com)

import os, sqlite3

db = "solsaleswatch.db"

# If database doesn't yet exist, initialize it with the table structure
if not os.path.isfile(db):
    print "No database found; initializing \'" + db + "\'..."
    # Initialize database
    dbconn = sqlite3.connect(db)
    dbc = dbconn.cursor()
    dbc.execute("CREATE TABLE transaction (name TEXT, collection TEXT, description TEXT, image_url TEXT, cost REAL, txid TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT)")
    dbconn.commit()
    dbconn.close()
