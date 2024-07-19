// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

contract TrainingPoW {
    struct Task {
        uint256 id;
        address miner;
        string datasetHash;
        string modelHash;
        bool completed;
        uint256 reward;
    }

    mapping(uint256 => Task) public tasks;
    uint256 public taskCount;
    address public owner;

    event TaskCreated(uint256 id, string datasetHash, string modelHash, uint256 reward);
    event TaskAssigned(uint256 id, address miner);
    event ResultSubmitted(uint256 id, string modelHash, uint256 accuracy);
    
    constructor() {
        owner = msg.sender;
    }

    function createTask(string memory datasetHash, string memory modelHash, uint256 reward) public {
        require(msg.sender == owner, "Only owner can create tasks");
        tasks[taskCount] = Task(taskCount, address(0), datasetHash, modelHash, false, reward);
        emit TaskCreated(taskCount, datasetHash, modelHash, reward);
        taskCount++;
    }

    function assignTask(uint256 taskId, address miner) public {
        require(tasks[taskId].miner == address(0), "Task already assigned");
        tasks[taskId].miner = miner;
        emit TaskAssigned(taskId, miner);
    }

    function submitResult(uint256 taskId, string memory modelHash, uint256 accuracy) public {
        require(tasks[taskId].miner == msg.sender, "Only assigned miner can submit results");
        tasks[taskId].completed = true;
        tasks[taskId].modelHash = modelHash;
        emit ResultSubmitted(taskId, modelHash, accuracy);

        // Calculate reward based on accuracy
        uint256 reward = calculateReward(taskId, accuracy);

        // Transfer reward to the miner
        payable(msg.sender).transfer(reward);
    }

    function calculateReward(uint256 taskId, uint256 accuracy) internal view returns (uint256) {
        if (accuracy >= 90) {
            return tasks[taskId].reward * 2; // Double reward for accuracy >= 90%
        } else if (accuracy >= 80) {
            return tasks[taskId].reward * 15 / 10; // 1.5x reward for accuracy >= 80%
        } else {
            return tasks[taskId].reward; // Base reward for lower accuracy
        }
    }

    function getCalculatedReward(uint256 taskId, uint256 accuracy) external view returns (uint256) {
        return calculateReward(taskId, accuracy);
    }
}
