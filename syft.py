import torch
import syft as sy
from torch import nn, optim

# Hook PyTorch
hook = sy.TorchHook(torch)

# Create virtual workers
alice = sy.VirtualWorker(hook, id="alice")
bob = sy.VirtualWorker(hook, id="bob")

# Define a simple model
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc = nn.Linear(784, 10)

    def forward(self, x):
        return self.fc(x)

# Create model and optimizer
model = Net()
optimizer = optim.SGD(model.parameters(), lr=0.1)

# Training function
def train(data, target, model, optimizer):
    model.send(data.location)
    optimizer.zero_grad()
    output = model(data)
    loss = nn.CrossEntropyLoss()(output, target)
    loss.backward()
    optimizer.step()
    return model

# Simulate data
data_alice = torch.randn((100, 784)).send(alice)
target_alice = torch.randint(0, 10, (100,)).send(alice)

data_bob = torch.randn((100, 784)).send(bob)
target_bob = torch.randint(0, 10, (100,)).send(bob)

# Train model on Alice's data
model = train(data_alice, target_alice, model, optimizer)

# Train model on Bob's data
model = train(data_bob, target_bob, model, optimizer)

# Get model back from Bob
model = model.get()

print("Model trained on Alice's and Bob's data and retrieved successfully.")
