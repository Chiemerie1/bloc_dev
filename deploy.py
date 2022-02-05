import os
import json
from solcx import compile_standard, install_solc
from web3 import Web3
from dotenv import load_dotenv
 
load_dotenv()


with open("./SimpleStorage.sol", "r") as simple_storage_file:
    simple_storage_file = simple_storage_file.read()
    print(simple_storage_file)

packaged = compile_standard({
    "language": "Solidity",
    "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
    "settings": {"outputSelection":{"*":{"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}}}
},
solc_version="0.6.0"
)
install_solc("0.6.0")
print(packaged)

# saving the compiled file in a Json format

# with open("compiled_solidity.json", "w") as file:
#     json.dump(packaged, file)

# getting contract abi and byte code.
bytecode = packaged["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
abi = packaged["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

web_3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_ID = 1337
cont_addr = "0xB520244F395bA315F4327de4645a9574F00aBBD0"
private_key = os.environ.get("PRIVATE_KEY")
print(private_key) ##### for debug sake

# creating the transacton/contract in python.
SimpleStorage = web_3.eth.contract(abi=abi, bytecode=bytecode)

# # getting the last transaction
nonce = web_3.eth.getTransactionCount(cont_addr)
print(nonce)

# # Building a trnsaction
txn = SimpleStorage.constructor().buildTransaction(
    {
    "chainId": chain_ID,
    "gasPrice": web_3.eth.gas_price,
    "from": cont_addr,
    "nonce": nonce,
    }
)
print(txn)

# Signing the transaction
signed_txn = web_3.eth.account.sign_transaction(txn, private_key=private_key)
print(signed_txn)

# Sending the signed txn
txn_hash = web_3.eth.send_raw_transaction(signed_txn.rawTransaction)

hash_rate = web_3.eth.hashrate
gas_price = web_3.eth.gas_price

def transaction_info(hash_rate, gas_price):
    print(gas_price/(10**18))
    print(hash_rate)

transaction_info(hash_rate, gas_price)

# waiting for block confirmation
'''
The confirm trxn "web_3.eth.wait_for_transaction_receipt"
has the transaction info eg. the contact address
'''
confirm_trxn  = web_3.eth.wait_for_transaction_receipt(txn_hash)

# Working with the contract

simple_storage = web_3.eth.contract(address=confirm_trxn.contractAddress, abi=abi)
print(simple_storage.functions.retrieve().call())

print(simple_storage.functions.store(20).call()) # the call() fn does not make a state change.

'''
making a state change in the contract requires building the transaction (again)
'''











