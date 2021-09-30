from solcx import compile_standard, install_solc
import json
import os
from web3 import Web3
from dotenv import load_dotenv  # for private key (.env file)

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

print("Installing...")
install_solc("0.6.0")

# Compile our Solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
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

with open("compiled_sol.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode from compile_sol.json
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get ABI from compile_sol.json
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to ganache
# w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
# chain_id = 1337
# my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
# private_key = os.getenv("PRIVATE_KEY")
# print(private_key)

# for connecting to Rinkeby

w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/d1dbebcb99594cd9900027838fdff0eb")
)
chain_id = 4
my_address = "0x015Eb143584DfdD38D4605c73D601F41d02525Cf"  # get it from metamask
private_key = os.getenv("PRIVATE_KEY")
print(private_key)


# Create contract in phyton
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get latest transaction
nonce = w3.eth.getTransactionCount(my_address)
# Build Transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)
# Sign Transaction with private key
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# Send Transaction
print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# Transaction confirmation
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")

#################################################################
# Working with contract

# Contract address, Contract ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Call -> Simulate making a call and getting return value (no state change)
# Transact -> Actually making a state change
print(
    # Initial value of favorite number
    simple_storage.functions.retrieve().call()
)  # use call because retrieve func is view

# print(simple_storage.functions.store(15).call())
print("Updating contract...")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce + 1}
)

# sign txn
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
# send txn
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
# txn confirmation
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

print("Updated!")

print(
    # Initial value of favorite number
    simple_storage.functions.retrieve().call()
)
