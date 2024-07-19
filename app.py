from flask import Flask, render_template, request, redirect, url_for
from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Connect to the blockchain
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))  # Adjust port if needed
contract_address = os.getenv('CONTRACT_ADDRESS')
owner_address = os.getenv('OWNER_ADDRESS')
owner_private_key = os.getenv('OWNER_PRIVATE_KEY')

# Load contract ABI
with open('build/contracts/TrainingPoW.json') as f:
    contract_abi = json.load(f)['abi']
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

@app.route('/')
def index():
    tasks = contract.functions.taskCount().call()
    task_list = []
    for i in range(tasks):
        task = contract.functions.tasks(i).call()
        task_list.append(task)
    return render_template("index.html", tasks=task_list)

@app.route('/create_task', methods=['POST'])
def create_task():
    dataset_hash = request.form['dataset_hash']
    model_hash = request.form['model_hash']
    reward = int(request.form['reward'])

    create_task_tx = contract.functions.createTask(dataset_hash, model_hash, reward).build_transaction({
        'chainId': 1,
        'gas': 1000000,
        'gasPrice': web3.to_wei('20', 'gwei'),  
        'nonce': web3.eth.get_transaction_count(owner_address),
    })
    signed_tx = web3.eth.account.sign_transaction(create_task_tx, private_key=owner_private_key)
    web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    return redirect(url_for('index'))

@app.route('/assign_task', methods=['POST'])
def assign_task():
    task_id = int(request.form['task_id'])
    miner_address = request.form['miner_address']

    assign_task_tx = contract.functions.assignTask(task_id, miner_address).build_transaction({
        'chainId': 1,
        'gas': 70000,
        'gasPrice': web3.to_wei('20', 'gwei'),  
        'nonce': web3.eth.get_transaction_count(owner_address),
    })
    signed_tx = web3.eth.account.sign_transaction(assign_task_tx, private_key=owner_private_key)
    web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    return redirect(url_for('index'))

@app.route('/submit_result', methods=['POST'])
def submit_result():
    task_id = int(request.form['task_id'])
    model_hash = request.form['model_hash']
    accuracy = int(request.form['accuracy'])
    miner_private_key = 'your_miner_private_key_here'  # Change this to the actual miner's private key

    submit_result_tx = contract.functions.submitResult(task_id, model_hash, accuracy).build_transaction({
        'chainId': 1,
        'gas': 70000,
        'gasPrice': web3.to_wei('20', 'gwei'),  
        'nonce': web3.eth.get_transaction_count(owner_address),
    })
    print(f'Sumbit Result tx output for error debug: {submit_result_tx}')
    signed_tx = web3.eth.account.sign_transaction(submit_result_tx, private_key=miner_private_key)
    web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
