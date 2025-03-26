# Define a simple model with two linear layers
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
class SimpleModel(nn.Module):
    def __init__(self, num_features):
        super(SimpleModel, self).__init__()
        self.layer1 = nn.Linear(num_features, 64)  # 64 output units
        self.layer2 = nn.Linear(64, 1)   # 64 input units, 1 output value

    def forward(self, x):
        x = torch.relu(self.layer1(x))  # Apply ReLU activation after first layer
        x = self.layer2(x)              # Output layer
        return x
numFeatures = 26
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