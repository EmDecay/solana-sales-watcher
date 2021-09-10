# Mint Address - Pigv3gFWLWJL8QwrFBkdZLe1RYzNJTSJPGEUNVimJjh
# Mainnet Beta RPC Endpoint:  https://api.mainnet-beta.solana.com || https://explorer-api.mainnet-beta.solana.com

import requests, json

request_sig = {"jsonrpc": "2.0", "id": 1, "method": "getConfirmedSignaturesForAddress2", "params": ["Pigv3gFWLWJL8QwrFBkdZLe1RYzNJTSJPGEUNVimJjh"]}
response_sig = requests.post("https://explorer-api.mainnet-beta.solana.com", json=request_sig)
sig = json.loads(response_sig.text)["result"][0]["signature"]

request_price = {"jsonrpc": "2.0", "id": 1, "method": "getConfirmedTransaction", "params": [sig]}
response_price= requests.post("https://explorer-api.mainnet-beta.solana.com", json=request_price)
price_before = json.loads(response_price.text)["result"]["meta"]["preBalances"][0]
price_after = json.loads(response_price.text)["result"]["meta"]["postBalances"][0]

print (sig + " --- " + str(price_before/1000000000) + " --- " + str(price_after/1000000000))