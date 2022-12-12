#3:44:22

from solcx import compile_standard, install_solc #solidity compiler in python
import json
import os
from dotenv import load_dotenv
from web3 import Web3

#Load .env files
load_dotenv()

## GRABE SMART CONTRACT FILE #################################
with open("smartStorage.sol", "r") as file:
    simple_storage_file = file.read()
    #print(simple_storage_file)

## Install solidity compiler #################################
print("Installing...")
install_solc("0.6.0")

## COMPILE SMART CONTRACT FILE #################################

print("Installing Compiler...")
install_solc("0.6.0")
print("CompilerInstalled !")

# Extract compiled smart contract
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

#print(compiled_sol)

## GRABE SMART CONTRACT AS JSON FILE #################################
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

## EXTRACT BYTECODE AND ABI #################################
# get bytecode
bytecode = compiled_sol["contracts"]["smartStorage.sol"]["smartStorage"]["evm"]["bytecode"]["object"]

# get abi
abi = json.loads(compiled_sol["contracts"]["smartStorage.sol"]["smartStorage"]["metadata"])["output"]["abi"]

## SET BLOCKCHAIN CONNECTIONS VARIABLES #################################
Ganache_gui_url = "HTTP://127.0.0.1:7545"
Ganache_cli_url = "HTTP://127.0.0.1:8545"
infura_cli_url = "https://goerli.infura.io/v3/48ee1345cc204db38ca412dcffbc44ca"

RPC_SERVER = infura_cli_url
chain_id = 5 # chainid.network to chech network's chainId
NETWORK_ID = chain_id
PUBLIC_KEY = os.getenv("PUBLIC_KEY")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
MY_ADDRESS = PUBLIC_KEY

## CREATE CONTRACT IN PYTHON WITH WEB3 LIBRARY #################################
w3 = Web3(Web3.HTTPProvider(RPC_SERVER))
smartStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
#print(smartStorage)

# Get the latest transaction
nonce = w3.eth.getTransactionCount(MY_ADDRESS)
#print(nonce)

## MAKE THE TRANSACTION THAT DEPLOY THE CONTRACT #################################
# 1. Build a Transaction
transaction = smartStorage.constructor().buildTransaction(
    {
        "chainId": NETWORK_ID,
        "gasPrice": w3.eth.gas_price,
        "from": MY_ADDRESS,
        "nonce": nonce,
    }
)
#print(transaction)

# 2. sign the Transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
print("Deploying Contract!")
#print(signed_txn)

# 3. Send the transaction to the block!
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction) 

#Wait for block confirmations 
print("Updating stored Value...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Contract Deployed !")


## WORKING WITH THE CONTRACT #################################
# To work with the contract, you always need : 
# 1. Contract Address and  
# 2. Contract ABI (Application Binary Interface)
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

## INTERACT WITH EXISTING CONTRACT #################################
# we have 2 ways to interact with a contract :
# 1. with a call -> Simulate making the call and getting the return value (Calls don't make a state change)
# 2. with a transact -> make a state change


# Initialize value of favorite number
print(simple_storage.functions.retrieve().call())
#print(simple_storage.functions.store(15).call())

## UPDATE A CONTRACT #################################
print("Updating Contract !")
# build Tx
store_transaction = simple_storage.functions.store(15).buildTransaction(
   {
        "chainId": NETWORK_ID,
        "gasPrice": w3.eth.gas_price,
        "from": MY_ADDRESS,
        "nonce": nonce + 1,
    } 
)

# sign Tx
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, 
    private_key=PRIVATE_KEY
)

# send Tx
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)

#grabe Tx receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Contract Updated !")
print(simple_storage.functions.retrieve().call())




 