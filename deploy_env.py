import json
import os
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Constants
GANACHE_URL = 'http://127.0.0.1:8545'
CONTRACT_PATH = './build/contracts/TrainingPoW.json'  # Ensure this path is correct
GAS_LIMIT = 3000000

def main():
    # Connect to Ganache
    web3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    
    if not web3.is_connected():
        print("Failed to connect to Ganache")
        return

    # Get the first account as the owner
    owner_address = web3.eth.accounts[0]
    owner_private_key = '0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d'  # Corresponding private key from Ganache output

    # Load the contract
    with open(CONTRACT_PATH, 'r') as file:
        contract_data = json.load(file)

    contract_abi = contract_data['abi']
    contract_bytecode = contract_data['bytecode']

    # Deploy the contract
    contract = web3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
    tx_hash = contract.constructor().transact({'from': owner_address, 'gas': GAS_LIMIT})
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = tx_receipt.contractAddress

    # Print the results
    print(f"Contract Address: {contract_address}")
    print(f"Owner Address: {owner_address}")
    print(f"Owner Private Key: {owner_private_key}")

    # Save to environment variables or a file
    os.environ['CONTRACT_ADDRESS'] = contract_address
    os.environ['OWNER_ADDRESS'] = owner_address
    os.environ['OWNER_PRIVATE_KEY'] = owner_private_key

    # Optionally, write to a file
    with open('.env', 'w') as env_file:
        env_file.write(f"CONTRACT_ADDRESS={contract_address}\n")
        env_file.write(f"OWNER_ADDRESS={owner_address}\n")
        env_file.write(f"OWNER_PRIVATE_KEY={owner_private_key}\n")

if __name__ == "__main__":
    main()
