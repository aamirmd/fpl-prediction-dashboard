# Define a simple model with two linear layers
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
class SimpleModelOld(nn.Module):
    def __init__(self, num_features):
        super(SimpleModel, self).__init__()
        self.layer1 = nn.Linear(num_features, 64)  # 64 output units
        self.layer2 = nn.Linear(64, 1)   # 64 input units, 1 output value

    def forward(self, x):
        x = torch.relu(self.layer1(x))  # Apply ReLU activation after first layer
        x = self.layer2(x)              # Output layer
        return x
    
class ResidualBlock(nn.Module):
    def __init__(self, dim, dropout=0.1):
        super().__init__()
        self.fc1 = nn.Linear(dim, dim)
        self.fc2 = nn.Linear(dim, dim)
        self.norm1 = nn.LayerNorm(dim)
        self.norm2 = nn.LayerNorm(dim)
        self.dropout = nn.Dropout(dropout)
        self.activation = nn.LeakyReLU(0.1)

    def forward(self, x):
        residual = x
        out = self.fc1(self.norm1(x))
        out = self.activation(out)
        out = self.dropout(out)
        out = self.fc2(self.norm2(out))
        return self.activation(out + residual)

# Define a more complex model
class SimpleModel(nn.Module):
    def __init__(self, num_features, output_dim=1, hidden_dim=128, num_blocks=3, dropout=0.1):
        super(SimpleModel, self).__init__()
        self.input_layer = nn.Linear(num_features, hidden_dim)
        self.blocks = nn.Sequential(*[
            ResidualBlock(hidden_dim, dropout) for _ in range(num_blocks)
        ])
        self.output_layer = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        x = self.input_layer(x)
        x = self.blocks(x)
        return self.output_layer(x)
numFeatures = 21
# To load the model
""" model = SimpleModel(numFeatures)
model.load_state_dict(torch.load('./models/baseline.pth'))
model.eval()  # Set to evaluation mode before inference

# 2. Prepare the test dataset
# Assuming you have test data as NumPy arrays
test_inputs = [x for x in range(26)]
# Note: Replace with your actual test data

# Convert test inputs to torch tensors
test_inputs_tensor = torch.tensor(test_inputs, dtype=torch.float32)

# 3. Run inference on the test data
with torch.no_grad():  # Disables gradient calculation for inference
    predictions = model(test_inputs_tensor)

# 4. Process the predictions
# The predictions will be of shape [10, 1] (1 output per sample)
# If you need to convert it to a more readable format (e.g., as NumPy array)
predictions_np = predictions.numpy()

# 5. Output the results
print("Predictions for test dataset:")
print(predictions_np) """