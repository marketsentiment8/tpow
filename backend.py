from web3 import Web3
from syft import VirtualWorker
import json

# Connect to the blockchain
web3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
contract_address = 'your_contract_address'
with open('TrainingPoW.json') as f:
    contract_abi = json.load(f)
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Initialize PySyft worker
worker = VirtualWorker(hook, id="worker")

def create_task(dataset_hash, model_hash, reward, owner_private_key):
    create_task_tx = contract.functions.createTask(dataset_hash, model_hash, reward).buildTransaction({
        'chainId': 1,
        'gas': 70000,
        'nonce': web3.eth.getTransactionCount(owner_address),
    })
    signed_tx = web3.eth.account.signTransaction(create_task_tx, private_key=owner_private_key)
    web3.eth.sendRawTransaction(signed_tx.rawTransaction)

def assign_task(task_id, miner_address, owner_private_key):
    assign_task_tx = contract.functions.assignTask(task_id, miner_address).buildTransaction({
        'chainId': 1,
        'gas': 70000,
        'nonce': web3.eth.getTransactionCount(owner_address),
    })
    signed_tx = web3.eth.account.signTransaction(assign_task_tx, private_key=owner_private_key)
    web3.eth.sendRawTransaction(signed_tx.rawTransaction)

def submit_result(task_id, model_hash, accuracy, miner_private_key):
    submit_result_tx = contract.functions.submitResult(task_id, model_hash, accuracy).buildTransaction({
        'chainId': 1,
        'gas': 70000,
        'nonce': web3.eth.getTransactionCount(miner_address),
    })
    signed_tx = web3.eth.account.signTransaction(submit_result_tx, private_key=miner_private_key)
    web3.eth.sendRawTransaction(signed_tx.rawTransaction)
