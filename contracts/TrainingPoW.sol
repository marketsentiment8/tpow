// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

contract TrainingPoW {
    struct Task {
        uint id;
        string datasetHash;
        string modelHash;
        uint reward;
        address assignedMiner;
        uint accuracy;
    }

    Task[] public tasks;
    mapping(address => bool) public computePool;

    function createTask(string memory datasetHash, string memory modelHash, uint reward) public {
        tasks.push(Task(tasks.length, datasetHash, modelHash, reward, address(0), 0));
    }

    function assignTask(uint taskId, address miner) public {
        require(computePool[miner], "Miner not in compute pool");
        tasks[taskId].assignedMiner = miner;
    }

    function submitResult(uint taskId, string memory modelHash, uint accuracy) public {
        require(tasks[taskId].assignedMiner == msg.sender, "Not assigned miner");
        tasks[taskId].modelHash = modelHash;
        tasks[taskId].accuracy = accuracy;
    }

    function enterPool(address miner) public {
        computePool[miner] = true;
    }

    function getTaskAccuracy(uint taskId) public view returns (uint) {
        return tasks[taskId].accuracy;
    }
}
