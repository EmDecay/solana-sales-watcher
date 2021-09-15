# Pig Mint Address - Pigv3gFWLWJL8QwrFBkdZLe1RYzNJTSJPGEUNVimJjh
# TBT Mint Address - BVpxLszd8FLUd7N8trW2Ykq47PNHEojMpEu2qqy9KX1S
# Mainnet Beta RPC Endpoint:  https://api.mainnet-beta.solana.com || https://explorer-api.mainnet-beta.solana.com

import requests, json, base64, base58
from solana.publickey import PublicKey
from solana.rpc.api import Client
from metaplex_decoder import *
from solsalesdb import *

sol_client = Client("https://explorer-api.mainnet-beta.solana.com")
program_id = PublicKey("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s")

# Pig
# request_sig = {"jsonrpc": "2.0", "id": 1, "method": "getConfirmedSignaturesForAddress2", "params": ["Pigv3gFWLWJL8QwrFBkdZLe1RYzNJTSJPGEUNVimJjh"]}

# TBT
request_sig = {"jsonrpc": "2.0", "id": 1, "method": "getConfirmedSignaturesForAddress2", "params": ["BVpxLszd8FLUd7N8trW2Ykq47PNHEojMpEu2qqy9KX1S"]}
response_sig = requests.post("https://explorer-api.mainnet-beta.solana.com", json=request_sig)
sig = json.loads(response_sig.text)["result"][0]["signature"]

request_price = {"jsonrpc": "2.0", "id": 1, "method": "getConfirmedTransaction", "params": [sig]}
response_price = json.loads(requests.post("https://explorer-api.mainnet-beta.solana.com", json=request_price).text)["result"]["meta"]
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
print (nft_details)

nft_name = nft_details["name"]
nft_imageurl = nft_details["image"]
nft_exturl = nft_details["external_url"]
nft_description = nft_details["description"]
nft_cost = balance_difference/1000000000
nft_tx = sig

print("Signature: " + sig \
    + "\nStarting Balance: " + str(balance_before/1000000000) \
    + " SOL\nEnding Balance: " + str(balance_after/1000000000) \
    + " SOL\nCost: " + str(balance_difference/1000000000) \
    + " SOL\nMint: " + mint \
    + "\nNFT: " + nft_details["name"] \
    + "\nImage: " + nft_details["image"])

dbinit()
addtx(nft_tx, nft_name, nft_exturl, nft_description, nft_imageurl, nft_cost)