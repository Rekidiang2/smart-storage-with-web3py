import json
from web3 import Web3
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv
from web3.middleware import geth_poa_middleware
load_dotenv()

# Read contract file
with open("./smartStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Intall solidity compiler specific version 
print("Installing...")
install_solc("0.6.0")

# Smart compilation
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"smartStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

# Write compiled smart contract as json file
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["smartStorage.sol"]["smartStorage"]["evm"][
    "bytecode"
]["object"]

# get abi (Application Binary Interface)
abi = json.loads(
    compiled_sol["contracts"]["smartStorage.sol"]["smartStorage"]["metadata"]
)["output"]["abi"]

# For connecting to Goerli testnet via infura
# w3 = Web3(Web3.HTTPProvider(os.getenv("GOERLI_RPC_URL")))
# chain_id = 4

# For connecting to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337

if chain_id == 4:
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    print(w3.clientVersion)
#Added print statement to ensure connection suceeded as per
#https://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority

my_address = "0xC3e7f05fAbca552B77166D3512E5B15F9A4e3F75"
private_key = "0xec9b9c310bd9e0be44f9800c7808ef377c4d6bcf68922fb735575d155b5bd119"

# Create the contract in Python
smartStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# Submit the transaction that deploys the contract
transaction = smartStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)

# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")

# Send to the blockchain
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed at {tx_receipt.contractAddress}")

# Working with deployed Contracts
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Display current stored value 
print(f"Initial Stored Value {simple_storage.functions.retrieve().call()}")

# Update stored value
greeting_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)

signed_greeting_txn = w3.eth.account.sign_transaction(
    greeting_transaction, private_key=private_key
)

tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
print("Updating stored Value...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)

print(simple_storage.functions.retrieve().call())