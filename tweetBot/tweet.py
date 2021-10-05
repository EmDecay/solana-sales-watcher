import os, sqlite3, schedule, time, tweepy, requests, random, secrets, sys
# import dotENV

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
    #Setup access to Twitter API via Tweepy
    #auth = tweepy.OAuthHandler(secrets.CONSUMER_API_KEY, secrets.CONSUMER_API_SK)
    #auth.set_access_token(secrets.ACCESS_TOKEN, secrets.ACCESS_TOKEN_SK)
    #api = tweepy.API(auth)

    for row in untweeted():
        print(f"tweeting about {row[2]}")
        # twitter code goes here
        
        filename = 'temp.jpg'
        request = requests.get(row[6], stream=True)

        if request.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)

            # Consider moving all of this out of the download image block
            # Should tweets without images go out?
            #image = api.media_upload(filename)
            #nft_name = " ".join(row[2].split("_")) # this is for wool cap ONLY
            nft_name = row[2]
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
            #api.update_status(status=status,media_ids=[image.media_id_string])
            os.remove(filename)
        else:
            print("Unable to download image")

        # print(f"deleting id: {row[11]}")
        # dbc.execute("DELETE FROM tx WHERE uid='" + str(row[11]) + "'" )
        # DONT DELETE ROWS - FLIP THE DAMN FLAG - UNTESTED
        #print(f"Updating row uid {nft_db_uid}")
        #dbc.execute(f"UPDATE tx SET tweeted='yes' WHERE uid={nft_db_uid}") 

        #print("committing to db")
        #dbconn.commit()

    #print ("closing db")
    #dbconn.close()

if __name__ == "__main__":
    sys.path.append(os.path.dirname(sys.path[0]) + "/shared")
    from solsalesdbio import *
    schedule.every(15).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)   