import json
from web3 import Web3
from solcx import compile_standard, install_solc

# 1. Install the specific Solidity compiler version
print("Installing Solidity Compiler...")
install_solc('0.8.0')

# 2. Read the Solidity file
with open("./Voting.sol", "r") as file:
    voting_file = file.read()

# 3. Compile the Solidity Code
print("Compiling Contract...")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"Voting.sol": {"content": voting_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.0",
)

# 4. Extract the Bytecode (machine code) and ABI (interface)
bytecode = compiled_sol["contracts"]["Voting.sol"]["Voting"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["Voting.sol"]["Voting"]["abi"]

# 5. Connect to Ganache
# Ensure this matches the RPC SERVER address at the top of your Ganache App
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337

if w3.is_connected():
    print("Connected to Ganache Blockchain")
else:
    print("Failed to connect to Ganache")
    exit()

# ---------------------------------------------------------------------------
# TODO: REPLACE THESE WITH YOUR GANACHE VALUES
my_address = "YOUR_GANACHE_ADDRESS_HERE" 
private_key = "YOUR_PRIVATE_KEY_HERE"
# ---------------------------------------------------------------------------

# 6. Build the Transaction to Deploy
print("Deploying Contract...")
Voting = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the nonce (transaction count)
nonce = w3.eth.get_transaction_count(my_address)

# Build transaction
transaction = Voting.constructor().build_transaction({
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce,
    "gasPrice": w3.eth.gas_price
})

# 7. Sign the Transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# 8. Send the Transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Contract Deployed! Address: {tx_receipt.contractAddress}")

# 9. Save the Address and ABI to use in our App later
data = {
    "abi": abi,
    "contract_address": tx_receipt.contractAddress
}

with open("contract_data.json", "w") as outfile:
    json.dump(data, outfile)

print("Deployment Successful. Data saved to contract_data.json")