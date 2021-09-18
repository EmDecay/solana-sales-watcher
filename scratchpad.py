# solsaleswatch.py - The brains behind the code
# Author - Matt (emdecay (at) protonmail.com)

# Pig Address - Pigv3gFWLWJL8QwrFBkdZLe1RYzNJTSJPGEUNVimJjh
# TBT Address - BVpxLszd8FLUd7N8trW2Ykq47PNHEojMpEu2qqy9KX1S
# Panda Street Update Authority Address - J6JPuP91cRdPEWYWN1isvctDGXBEuV7azq1BZAb2dsJX

# Mainnet Beta RPC Endpoints:  https://api.mainnet-beta.solana.com || https://explorer-api.mainnet-beta.solana.com

import requests, json, base64, base58, yfinance
from solana.publickey import PublicKey
from solana.rpc.api import Client
from metaplex_decoder import *
from solsalesdbio import *

dbinit()

sol_client = Client("https://explorer-api.mainnet-beta.solana.com")
program_id = PublicKey("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s")

solusd = yfinance.Ticker("SOL1-USD").info["regularMarketPrice"]


# Pig
request_sig = {"jsonrpc": "2.0", "id": 1, "method": "getConfirmedSignaturesForAddress2", "params": ["Pigv3gFWLWJL8QwrFBkdZLe1RYzNJTSJPGEUNVimJjh"]}

# Panda Street
# request_sig = {"jsonrpc": "2.0", "id": 1, "method": "getConfirmedSignaturesForAddress2", "params": ["J6JPuP91cRdPEWYWN1isvctDGXBEuV7azq1BZAb2dsJX"]}

# TBT
# request_sig = {"jsonrpc": "2.0", "id": 1, "method": "getConfirmedSignaturesForAddress2", "params": ["BVpxLszd8FLUd7N8trW2Ykq47PNHEojMpEu2qqy9KX1S"]}

try:
    response_sig = requests.post("https://explorer-api.mainnet-beta.solana.com", json=request_sig)
    sig = json.loads(response_sig.text)["result"][0]["signature"]
    
    request_price = {"jsonrpc": "2.0", "id": 1, "method": "getConfirmedTransaction", "params": "Utdc3nvRHfK3S66oUpUzKag9e9SJhBSMbNLhUFcTmwC6BxKxh6gP8fqtWoUDD9ofzkL1fKqS3fC58pmGAnkWvRE"}
    response_price_full = json.loads(requests.post("https://explorer-api.mainnet-beta.solana.com", json=request_price).text)["result"]
    findmarketplace(json.dumps(response_price_full))
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

except Exception:
    print("Error")

def findmarketplace(sig):
    print(sig)