# solsaleswatch.py - The brains behind the code
# Author - Matt (emdecay (at) protonmail.com)

# Pig Update Authority Address - Pigv3gFWLWJL8QwrFBkdZLe1RYzNJTSJPGEUNVimJjh
# TBT Update Authority Address - BVpxLszd8FLUd7N8trW2Ykq47PNHEojMpEu2qqy9KX1S
# Panda Street Update Authority Address - J6JPuP91cRdPEWYWN1isvctDGXBEuV7azq1BZAb2dsJX

# Mainnet Beta RPC Endpoints:  https://api.mainnet-beta.solana.com || https://explorer-api.mainnet-beta.solana.com

import requests, json, base64, base58, yfinance, sqlite3, threading, queue
from solana.publickey import PublicKey
from solana.rpc.api import Client
from metaplex_decoder import *
from solsalesdbio import *

# Global variables used throughout the code
numlookups = 999
auth_address = "BVpxLszd8FLUd7N8trW2Ykq47PNHEojMpEu2qqy9KX1S"
sol_client = Client("https://explorer-api.mainnet-beta.solana.com")
program_id = PublicKey("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s")
solusd = yfinance.Ticker("SOL1-USD").info["regularMarketPrice"]
debug = True
verbose = True

# Global lookups used throughout the code
request_sig = {"jsonrpc": "2.0", "id": 1, "method": "getConfirmedSignaturesForAddress2", "params": [auth_address]}
response_sig = requests.post("https://explorer-api.mainnet-beta.solana.com", json=request_sig, timeout=10)

# findmarketplace(data)->marketplace - Determine and return the marketplace that a given transaction took place in
def findmarketplace(data):
    marketplace = "UNKN"

    for record in data["transaction"]["message"]["accountKeys"]:
        if record == "3iYf9hHQPciwgJ1TCjpRUp1A3QW4AfaK7J6vCmETRMuu":
            marketplace = "DEYE"
        elif record == "2NZukH2TXpcuZP4htiuT8CFxcaQSWzkkR6kepSWnZ24Q":
            marketplace = "MEDN"
        elif record == "E6dkaYhqbZN3a1pDrdbajJ9D8xA66LBBcjWi6dDNAuJH":
            marketplace = "SART"
    return marketplace

# Queue and threading setup
botQueue = queue.Queue(0)
botQueueLock = threading.Lock()
botThreads = []
maxThreads = 5

class solThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        txlookup()

def _txlookup(num):
    txnum = 0
    curThreadCount = 0

    # Create and populate the queue
    botQueueLock.acquire()
    while txnum <= num:
        botQueue.put(txnum)
        txnum += 1
    botQueueLock.release()

    # Create and start the threads
    while curThreadCount < maxThreads:
        botThreads.append(solThread())
        botThreads[curThreadCount].start()
        curThreadCount += 1

    # Loop until the queue is empty
    while not botQueue.empty():
        pass

    for thread in botThreads:
        thread.join()
    
def txlookup():
    while not botQueue.empty():
        botQueueLock.acquire()
        if not botQueue.empty():
            txnum = botQueue.get()
            if debug:
                print("Got TXNUM " + str(txnum) + " from the queue")
            botQueueLock.release()
            try:
                sig = json.loads(response_sig.text)["result"][txnum]["signature"]

                request_price = {"jsonrpc": "2.0", "id": 1, "method": "getConfirmedTransaction", "params": [sig]}
                response_price_full = json.loads(requests.post("https://explorer-api.mainnet-beta.solana.com", json=request_price, timeout=10).text)["result"]
                response_price = response_price_full["meta"]
                balance_before = response_price["preBalances"][0]
                balance_after = response_price["postBalances"][0]
                balance_difference = abs((balance_after-balance_before))
                mint = response_price["postTokenBalances"][0]["mint"]
                seed = [bytes("metadata".encode()) , bytes(program_id), bytes(PublicKey(mint))]
                program_address, _ = PublicKey.find_program_address(seed, program_id)
                program_address_data = sol_client.get_account_info(program_address)
                program_data = program_address_data["result"]["value"]["data"][0]
                metadata = deserialize_metadata(base58.b58encode(base64.b64decode(program_data)).decode("utf-8"))
                uri = json.loads(metadata)["uri"]
                nft_details = json.loads(requests.get(uri).text)
                timestamp = response_price_full["blockTime"]

                nft_collection = json.loads(metadata)["symbol"]
                nft_name = nft_details["name"]
                nft_imageurl = nft_details["image"]
                nft_exturl = nft_details["external_url"]
                nft_description = nft_details["description"]
                nft_cost = balance_difference/1000000000
                nft_tx = sig
                marketplace = findmarketplace(response_price_full)

                if verbose:
                    print("Signature: " + sig \
                        + "\nCollection: " + nft_collection \
                        + "\nStarting Balance: " + str(balance_before/1000000000) \
                        + " SOL\nEnding Balance: " + str(balance_after/1000000000) \
                        + " SOL\nCost: " + str(balance_difference/1000000000) \
                        + " SOL\nMint: " + mint \
                        + "\nCost (USD): " + str(solusd * (balance_difference/1000000000)) \
                        + "\nNFT: " + nft_details["name"] \
                        + "\nImage: " + nft_details["image"] \
                        + "\nMarketplace: " + marketplace)

                if((not txexists(nft_tx)) and (nft_cost > 0.1)):
                    addtx(nft_tx, timestamp, nft_name, nft_exturl, nft_collection, nft_description, nft_imageurl, nft_cost, solusd, marketplace)
            except Exception:
                print("Error")
                continue
        else:
            botQueueLock.release()

if __name__ == "__main__":
    if debug:
        print("In __main__")
    _txlookup(numlookups)
