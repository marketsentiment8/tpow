const TPOW = artifacts.require("TrainingPoW");
const { keccak256 } = web3.utils;

contract("TrainingPoW", (accounts) => {
  let tpowInstance;

  before(async () => {
    tpowInstance = await TPOW.deployed();
  });

  it("should submit a model", async () => {
    const modelHash = keccak256("model1");
    const accuracy = 75;
    const taskId = 0; // Replace with actual task ID

    // Assign task to accounts[0]
    await tpowInstance.assignTask(taskId, accounts[0]);

    // Submit result
    await tpowInstance.submitResult(taskId, modelHash, accuracy);

    // Verify event emission or other assertions
    const resultSubmittedEvent = await tpowInstance.getPastEvents("ResultSubmitted", {
      filter: { modelHash: modelHash },
      fromBlock: 0,
    });
    assert.equal(resultSubmittedEvent.length, 1, "ResultSubmitted event not emitted");
    assert.equal(resultSubmittedEvent[0].returnValues.modelHash, modelHash, "Model hash incorrect");
    assert.equal(resultSubmittedEvent[0].returnValues.accuracy, accuracy.toString(), "Accuracy incorrect");
  });

  it("should assign a task and submit a model", async () => {
    const datasetHash = keccak256("dataset1");
    const modelHash = keccak256("model2");
    const accuracy = 80;
    const taskId = 1; // Replace with actual task ID

    // Create task
    await tpowInstance.createTask(datasetHash, modelHash, 60);

    // Assign task to accounts[0]
    await tpowInstance.assignTask(taskId, accounts[0]);

    // Submit result
    await tpowInstance.submitResult(taskId, modelHash, accuracy);

    // Verify event emission or other assertions
    const finalBalance = await web3.eth.getBalance(accounts[0]);
    console.log("Final Balance after submission:", finalBalance.toString());
  });

  it("should create a task, assign task, submit model, and calculate reward based on accuracy", async () => {
    const datasetHash = keccak256("dataset2");
    const modelHash = keccak256("model3");
    const accuracy = 90; // Higher accuracy
    const taskId = 2; // Replace with actual task ID

    // Create task
    await tpowInstance.createTask(datasetHash, modelHash, 60);

    // Assign task to accounts[0]
    await tpowInstance.assignTask(taskId, accounts[0]);

    // Submit result
    await tpowInstance.submitResult(taskId, modelHash, accuracy);

    // Calculate expected reward based on accuracy
    const expectedReward = await tpowInstance.getCalculatedReward(taskId, accuracy);

    // Verify the reward received by accounts[0]
    const finalBalance = await web3.eth.getBalance(accounts[0]);


    // Additional assertions as needed
  });
});
