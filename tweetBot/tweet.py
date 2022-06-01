import os, sqlite3, schedule, time, tweepy, requests, random, secrets, sys, uuid, argparse

# Argument parsing
_args = argparse.ArgumentParser()
_args.add_argument("--runonce", required=False, default=True, help="Run just once (otherwise loop every 15 seconds) (default: %(default)s)")
_args.add_argument("--verbose", required=False, default=True, help="Show verbose results (default: %(default)s)")
args = _args.parse_args()

runonce = eval(str(args.runonce))
verbose = eval(str(args.verbose))

# call to actions
cta = [
    "Welcome to the crew!",
    "GOOD BUY! - Read the road map yet?",
    "Have you heard about our billboard in Times Square yet?",
]   

def job():
    #Setup access to Twitter API via Tweepy
    auth = tweepy.OAuthHandler(secrets.CONSUMER_API_KEY, secrets.CONSUMER_API_SK)
    auth.set_access_token(secrets.ACCESS_TOKEN, secrets.ACCESS_TOKEN_SK)
    api = tweepy.API(auth)

    for row in untweeted():
        print(f"tweeting about {row[2]}")
        # twitter code goes here
        
        filename = str(uuid.uuid4()) + ".png"
        request = requests.get(row[6], stream=True)

        if request.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)

            # Field Order:  txid TEXT, timestamp INTEGER, name TEXT, exturl TEXT, collection TEXT, description TEXT, imageurl TEXT, cost FLOAT, marketplace TEXT, solusd FLOAT, tweeted TEXT, uid INTEGER PRIMARY KEY AUTOINCREMENT
            image = api.media_upload(filename)
            nft_name = row[2]
            nft_sol = round(row[7],2)
            nft_usd = round((row[9] * nft_sol),2)
            nft_marketplace = row[8]
            nft_tx = "https://solscan.io/tx/" + row[0]
            nft_ext_url = row[3]
            nft_db_uid = row[11]

            # Have a standard deviaion check for which to use regular or big - eventually...  (to do)
            nft_sale_text = { 
                "regular" : f"🔥 {nft_name} SOLD on {nft_marketplace}  for {nft_sol}◎ (${nft_usd}) 🔥",
                "big" : f"🚨 BIG SALE ALERT 🚨 \n {nft_name} SOLD on {nft_marketplace} for {nft_sol}◎ (${nft_usd})"
            }
            
            # Craft the status message
            status = f"""{nft_sale_text["regular"]}\n\n{random.choice(cta)}\n\nTransaction: {nft_tx}"""
            
            # Post the tweet
            print("Tweeting now!")
            print(status)
            api.update_status(status=status,media_ids=[image.media_id_string])
            os.remove(filename)
        else:
            print("Unable to download image")

        # Update the database to reflect that we are tweeting about this tx
        print(f"Updating row uid {nft_db_uid}")
        settweeted(nft_db_uid)

if __name__ == "__main__":
    sys.path.append(os.path.dirname(sys.path[0]) + "/shared")
    from solsalesdbio import *
    if runonce:
        job()
    else:
        schedule.every(15).seconds.do(job)
        while True:
            schedule.run_pending()
            time.sleep(1)   