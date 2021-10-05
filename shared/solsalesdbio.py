# solsalesdbio.py - Initialize the database connectivity for solSalesWatch
# Author - Matt (emdecay (at) protonmail.com)

import os, sqlite3, os, sys

# Database parameters
db = os.path.dirname(sys.path[0]) + "/shared/solsaleswatch.db"

# If database doesn't yet exist, initialize it with the table structure
def dbinit():
    if not os.path.isfile(db):
        print ("No database found; initializing \'" + db + "\'...")
        # Initialize database
        dbconn = sqlite3.connect(db)
        dbc = dbconn.cursor()
        dbc.execute("CREATE TABLE tx(txid TEXT, timestamp INTEGER, name TEXT, exturl TEXT, collection TEXT, description TEXT, imageurl TEXT, cost FLOAT, marketplace TEXT, solusd FLOAT, tweeted TEXT, uid INTEGER PRIMARY KEY AUTOINCREMENT)")
        dbconn.commit()
        dbconn.close()

def addtx(txid, timestamp, name, exturl, collection, description, imgurl, cost, solusd, marketplace):
    # INSERT INTO tx VALUES("txid", "name", "http://ext.url", "description", "http://image.url", 3.14159, NULL)
    dbconn = sqlite3.connect(db)
    dbc = dbconn.cursor()
    dbc.execute("INSERT INTO tx(txid, timestamp, name, exturl, collection, description, imageurl, cost, solusd, marketplace, tweeted) \
        VALUES ('" + txid + "', '" + str(timestamp) + "', '" + name + "', '" + exturl + "', '" + collection + "', '" + description + "', '" + imgurl + "', " + str(cost) + ", " + str(solusd) + ", '" + marketplace + "', 'no')")
    dbconn.commit()
    dbconn.close()
    return

def txexists(txid):
    dbconn = sqlite3.connect(db)
    dbc = dbconn.cursor()
    txsearch = dbc.execute("SELECT txid FROM tx WHERE txid = '" + txid + "'").fetchone()
    dbconn.close()
    if txsearch is None:
        return False
    else:
        return True

def untweeted():
    dbconn = sqlite3.connect(db)
    dbc = dbconn.cursor()
    untweeted_list = dbc.execute("SELECT * FROM tx WHERE tweeted='no'").fetchall()
    dbconn.close()
    return untweeted_list

def settweeted(uid):
    print("Placeholder")