import pandas as pd
import numpy as np
import ast
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib
from time import time
import matplotlib.pyplot as plt

# Start the timer
start_time = time()

# Load the data
df = pd.read_csv('dataset.csv')

# Prepare the feature matrix and target variable
X = pd.DataFrame(df['Feature_Vector'].apply(ast.literal_eval).tolist())
y = df['Evaluation']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the model
model = RandomForestRegressor(n_estimators=30, random_state=42)
model.fit(X_train, y_train)

# Save the model to a file
joblib.dump(model, 'chess_position_evaluator.pkl')

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate the Mean Absolute Error
mae = mean_absolute_error(y_test, y_pred)

# Print out performance metrics
print(f'Mean Absolute Error: {mae:.2f}')
print(f'Time elapsed: {(time() - start_time):.2f} seconds')

# --- Matplotlib Visualizations ---

# 1. Plot Actual vs Predicted Values
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--')  # Perfect predictions line
plt.xlabel('Actual Evaluation')
plt.ylabel('Predicted Evaluation')
plt.title('Actual vs Predicted Evaluation')
plt.show()

# 2. Plot the Error Distribution (Residuals)
errors = y_test - y_pred

plt.figure(figsize=(8, 6))
plt.hist(errors, bins=30, edgecolor='black', alpha=0.7)
plt.xlabel('Prediction Error (Actual - Predicted)')
plt.ylabel('Frequency')
plt.title('Distribution of Prediction Errors')
plt.show()
