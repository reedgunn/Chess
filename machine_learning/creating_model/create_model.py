import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

###############################################################################
# Step 1: Read and parse the CSV file
###############################################################################

print("Step 1: Reading and parsing the CSV file...")

csv_file = 'backend/machine_learning/imported_data/processed_imported_dataset.csv'

# We expect two columns: "FeatureVector" (string) and "Evaluation" (numeric)
df = pd.read_csv(csv_file, sep=';', nrows=1_000_000)  # use ; as the delimiter

# df['FeatureVector'] will be strings like "[0, 1, 2, ..., -1, -1]"
# We need to parse them into lists of integers.

def parse_feature_vector(feature_str):
    # Remove the surrounding brackets '[' and ']'
    feature_str = feature_str.strip()[1:-1]
    # Split by comma
    str_values = feature_str.split(',')
    # Convert each to int, stripping whitespace
    int_values = list(map(lambda x: int(x.strip()), str_values))
    return int_values

features = df['FeatureVector'].apply(parse_feature_vector).tolist()
targets = df['Evaluation'].values

# Convert to PyTorch tensors
X = torch.tensor(features, dtype=torch.float32)
y = torch.tensor(targets, dtype=torch.float32).view(-1, 1)

print(f"Parsed {len(X)} feature vectors, each of size {X.shape[1]}.")
print("Sample feature vector:", X[0])
print("Sample target (evaluation):", y[0])

###############################################################################
# Step 2: Split data into train and test sets
###############################################################################
print("\nStep 2: Splitting dataset into train and test sets...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Training set size: {len(X_train)}")
print(f"Test set size: {len(X_test)}")

###############################################################################
# Step 3: Create a neural network model in PyTorch
###############################################################################
print("\nStep 3: Building the neural network model...")

class ChessEvaluator(nn.Module):
    def __init__(self, input_size):
        super(ChessEvaluator, self).__init__()
        # Feel free to adjust layer sizes
        self.fc1 = nn.Linear(input_size, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 1)  # single output for regression

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

input_size = X.shape[1]  # number of features in each feature vector
model = ChessEvaluator(input_size)

# Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

print("Model architecture:\n", model)

###############################################################################
# Step 4: Define optimizer and loss function
###############################################################################
learning_rate = 0.001
optimizer = optim.Adam(model.parameters(), lr=learning_rate)
criterion = nn.MSELoss()

###############################################################################
# Step 5: Train the model
###############################################################################
print("\nStep 5: Training the model...")

num_epochs = 20
batch_size = 32

# Utility function for batching
def get_batches(X, y, batch_size):
    for i in range(0, len(X), batch_size):
        yield X[i:i+batch_size], y[i:i+batch_size]

for epoch in range(num_epochs):
    # Shuffle data each epoch
    perm = torch.randperm(len(X_train))
    X_train = X_train[perm]
    y_train = y_train[perm]
    
    epoch_loss = 0.0
    for X_batch, y_batch in get_batches(X_train, y_train, batch_size):
        # Move to device (CPU or GPU)
        X_batch = X_batch.to(device)
        y_batch = y_batch.to(device)

        # Forward pass
        outputs = model(X_batch)
        loss = criterion(outputs, y_batch)

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        epoch_loss += loss.item()

    avg_loss = epoch_loss / (len(X_train)//batch_size + 1)
    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {avg_loss:.4f}")

###############################################################################
# Step 6: Evaluate on the test set
###############################################################################
print("\nStep 6: Evaluating model on the test set...")
model.eval()
with torch.no_grad():
    X_test = X_test.to(device)
    y_test = y_test.to(device)
    predictions = model(X_test)
    test_loss = criterion(predictions, y_test).item()

print(f"Test MSE Loss: {test_loss:.4f}")

###############################################################################
# Step 7: Save/Export the model
###############################################################################
print("\nStep 7: Saving the model for later use...")

# Save just the state dictionary (weights) — recommended best practice:
torch.save(model.state_dict(), 'backend/machine_learning/chess_evaluator_state_dict.pth')

# Alternatively, save the entire model if you prefer:
# torch.save(model, 'chess_evaluator_full_model.pth')

print("Model has been saved as 'chess_evaluator_state_dict.pth'.")

###############################################################################
# Usage in other scripts:
#   - Recreate the model architecture:
#       model = ChessEvaluator(input_size)
#       model.load_state_dict(torch.load('chess_evaluator_state_dict.pth'))
#       model.eval()
#   - Then use `model(new_data)` for predictions.
###############################################################################

print("\nDone! The script has finished end-to-end execution.")
