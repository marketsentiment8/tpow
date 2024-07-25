from flask import Flask, render_template, request, redirect, url_for, jsonify
from web3 import Web3
import json
import os
from dotenv import load_dotenv
import syft as sy  # Import PySyft

load_dotenv()

app = Flask(__name__)

# Connect to the blockchain
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545')) 
contract_address = os.getenv('CONTRACT_ADDRESS')
owner_address = os.getenv('OWNER_ADDRESS')
owner_private_key = os.getenv('OWNER_PRIVATE_KEY')

# Load contract ABI
with open('build/contracts/TrainingPoW.json') as f:
    contract_abi = json.load(f)['abi']
contract = web3.eth.contract(address=contract_address, abi=contract_abi)


sy_domain = sy.Domain(name="ComputePool")

@app.route('/')
def index():
    tasks = contract.functions.taskCount().call()
    task_list = []
    for i in range(tasks):
        task = contract.functions.tasks(i).call()
        task_list.append(task)
    return render_template("index.html", tasks=task_list)

@app.route('/register_node', methods=['POST'])
def register_node():
    node_address = request.form['node_address']
    # Register the node with PySyft
    # Note: Actual implementation might involve more details like checking node status, capabilities, etc.
    sy_node = sy_domain.register_node(node_address)
    return jsonify({'status': 'Node registered successfully', 'node_id': sy_node.id})

@app.route('/create_task', methods=['POST'])
def create_task():
    dataset_url = request.form['dataset_url']
    model_code = request.form['model_code']  # Assuming model code is submitted as a string
    reward = int(request.form['reward'])

    create_task_tx = contract.functions.createTask(dataset_url, model_code, reward).build_transaction({
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
    node_id = request.form['node_id']

    # Assign task to node in PySyft
    task = sy_domain.assign_task(task_id, node_id)

    # Interact with the blockchain to record the assignment
    assign_task_tx = contract.functions.assignTask(task_id, node_id).build_transaction({
        'chainId': 1,
        'gas': 100000,
        'gasPrice': web3.to_wei('20', 'gwei'),  
        'nonce': web3.eth.get_transaction_count(owner_address),
    })
    signed_tx = web3.eth.account.sign_transaction(assign_task_tx, private_key=owner_private_key)
    web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    return jsonify({'status': 'Task assigned successfully', 'task_id': task.id})

@app.route('/submit_result', methods=['POST'])
def submit_result():
    task_id = int(request.form['task_id'])
    model_weights = request.form['model_weights']  # Assume weights are serialized and submitted
    accuracy = float(request.form['accuracy'])
    miner_private_key = request.form['miner_private_key']
    miner_address = request.form['miner_address']

    # Submit results via PySyft
    sy_domain.submit_task_result(task_id, model_weights, accuracy)

    # Record the result submission on the blockchain
    submit_result_tx = contract.functions.submitResult(task_id, model_weights, accuracy).build_transaction({
        'chainId': 1,
        'gas': 100000,
        'gasPrice': web3.to_wei('20', 'gwei'),
        'nonce': web3.eth.get_transaction_count(miner_address),
    })
    signed_tx = web3.eth.account.sign_transaction(submit_result_tx, private_key=miner_private_key)
    web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    return jsonify({'status': 'Result submitted successfully', 'task_id': task_id})

if __name__ == '__main__':
    app.run(debug=True)
