import requests

request = {"jsonrpc": "2.0", "id": 1, "method": "getTokenAccountsByOwner", "params": ["HWg3Si1kwdTUbhPUh8PcFaDVftPxPVD1VmMtwSLbHcTN", {"mint":"8MVSq9v2epf382CHfJdDomAvzA7qRVxVt64QBNFrWNuc"}, {"encoding":"jsonParsed"}]}
response = requests.post("https://explorer-api.mainnet-beta.solana.com", json=request)
print (response.text)