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
        dbc.execute("CREATE TABLE tx(name TEXT, exturl TEXT, collection TEXT, description TEXT, imageurl TEXT, cost FLOAT, txid TEXT, uid INTEGER PRIMARY KEY AUTOINCREMENT)")
        dbconn.commit()
        dbconn.close()

def addtx(txid, name, exturl, collection, description, imgurl, cost):
    # INSERT INTO tx VALUES("txid", "name", "http://ext.url", "description", "http://image.url", 3.14159, NULL)
    dbconn = sqlite3.connect(db)
    dbc = dbconn.cursor()
    dbc.execute("INSERT INTO tx(txid, name, exturl, collection, description, imageurl, cost) \
        VALUES ('" + txid + "', '" + name + "', '" + exturl + "', '" + collection + "', '" + description + "', '" + imgurl + "', " + str(cost) + ")")
    dbconn.commit()
    dbconn.close()
    return