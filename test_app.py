from unittest.mock import patch
import pytest

@pytest.fixture
def client():
    from app import app
    app.config['TESTING'] = True
    return app.test_client()

def test_index(client):
    with patch('app.contract') as mock_contract:
        mock_contract.functions.taskCount.return_value.call.return_value = 2
        mock_contract.functions.tasks.return_value.call.side_effect = [
            (1, "0xMiner1", "dataset_hash_1", "model_hash_1", True, 10),
            (2, "0xMiner2", "dataset_hash_2", "model_hash_2", False, 20)
        ]
        response = client.get('/')
        html_data = response.data.decode()

        # Print HTML for debugging
        print(html_data)

        # Check for specific elements in the HTML
        assert b'TrainingPoW DApp' in response.data
        assert b'Task List' in response.data
        assert b'Task ID: 1' in response.data
        assert b'Miner: 0xMiner1' in response.data
        assert b'Dataset Hash: dataset_hash_1' in response.data
        assert b'Model Hash: model_hash_1' in response.data
        assert b'Completed: True' in response.data
        assert b'Reward: 10' in response.data
        assert b'Task ID: 2' in response.data
        assert b'Miner: 0xMiner2' in response.data
        assert b'Dataset Hash: dataset_hash_2' in response.data
        assert b'Model Hash: model_hash_2' in response.data
        assert b'Completed: False' in response.data
        assert b'Reward: 20' in response.data
