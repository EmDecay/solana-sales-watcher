import os, sqlite3
import schedule, time
import tweepy
import requests 
import random
# import dotENV

# THESE SHOULD BE MOVED TO ENV OR SOMETHING
twitter_keys = {
    'consumer_key':        '',
    'consumer_secret':     '',
    'access_token_key':    '',
    'access_token_secret': ''
}

# call to actions - WC
cta = [
    "Another one has joined the herd! BAHHHHHHH! 🐑",
    "🐑🐑🐑🐑🐑🐑🐑🐑🐑🐑🐑🐑🐑🐑",
    "GOOD BUY! - Read the road map yet?",
    "OoOoOoOoo! This sheep is ready to get sheared!",
    "1 🐑 2 🐑 3 🐑 😴 gn",
    "🌞",
    "wagmi frens!",
    "Ready for tomfoolery!",
    "Have you heard about our billboard in times sq yet?",
    "The herd needs you!",
    "BAHHHHHHHHHHHHHH 🐑🐑🐑",
]   

def job():
    print("-----------Job started-----------")
    db = "solsaleswatch.db"
    dbconn = sqlite3.connect(db)
    print ("DB connected")
    dbc = dbconn.cursor()

    print ("Logging into twitter")
    #Setup access to API
    auth = tweepy.OAuthHandler(twitter_keys['consumer_key'], twitter_keys['consumer_secret'])
    auth.set_access_token(twitter_keys['access_token_key'], twitter_keys['access_token_secret'])

    api = tweepy.API(auth)
    print("If no error - we're good, lets roll")
    # print(api.verify_credentials())


    for row in dbc.execute('SELECT * FROM tx WHERE tweeted="no" LIMIT 1'):
        print(f"tweeting about {row[11]}")
        # twitter code goes here
        
        filename = 'temp.jpg'
        request = requests.get(row[6], stream=True)

        if request.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)

            # Consider moving all of this out of the download image block
            # Should tweets without images go out?
            image = api.media_upload(filename)
            nft_name = " ".join(row[2].split("_")) # this is for wool cap ONLY
            # nft_name = row[2] # THIS SHOULD WORK FOR EVERYONE ELSE THAT DOESNT NEED STRING SPLIT
            nft_sol = round(row[7],2)
            nft_usd = round(row[9],2)
            nft_marketplace = row[8]
            nft_tx = "https://solscan.io/tx/" + row[0]
            nft_ext_url = row[3]
            nft_db_uid = row[11]

            # Have a standard deviaion check for which to use regular or big
            nft_sale_text = { 
                "regular" : f"🔥 {nft_name} SOLD for {nft_sol}◎ (${nft_usd}) 🔥",
                "big" : f"🚨 BIG SALE ALERT 🚨 \n {nft_name} SOLD for {nft_sol} (${nft_usd})"
            }
            
            # Craft the status message
            status = f"""{nft_sale_text["regular"]}\n\n{random.choice(cta)}\n\ntx: {nft_tx}\n{nft_ext_url}\n#woolcapitalNFT #solana #NFT"""
            
            # Post the tweet
            print("Tweeting now!")
            print(status)
            api.update_status(status=status,media_ids=[image.media_id_string])
            os.remove(filename)
        else:
            print("Unable to download image")

        # print(f"deleting id: {row[11]}")
        # dbc.execute("DELETE FROM tx WHERE uid='" + str(row[11]) + "'" )
        # DONT DELETE ROWS - FLIP THE DAMN FLAG - UNTESTED
        print(f"Updating row uid {nft_db_uid}")
        dbc.execute(f"UPDATE tx SET tweeted='yes' WHERE uid={nft_db_uid}") 

        print("committing to db")
        dbconn.commit()

    print ("closing db")
    dbconn.close()

    print("-----------DONE-----------")
    

if __name__ == "__main__":
    schedule.every(15).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)   