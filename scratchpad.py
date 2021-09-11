from solana.rpc.api import Client
from solana.publickey import PublicKey
import solana

http_client = Client("https://explorer-api.mainnet-beta.solana.com")

pubkey = PublicKey(1)

# Seed values for list:
# 1 - "metadata"
# 2 - Public key/address of metaplex
# 3 - Mint account pub key

mint = "8MVSq9v2epf382CHfJdDomAvzA7qRVxVt64QBNFrWNuc"
program_id = PublicKey("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s")
seed = [bytes("metadata".encode()) , bytes(program_id), bytes(PublicKey(mint))]
program_address, _ = PublicKey.find_program_address(seed, program_id)
program_address_data = http_client.get_account_info(program_address)
program_data = program_address_data["result"]["value"]["data"][0]

print(program_data)