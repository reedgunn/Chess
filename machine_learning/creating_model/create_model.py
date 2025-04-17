import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import ast
import joblib

CSV_FILE_PATH = 'machine_learning/working_with_data/generated_data/generated_dataset.csv'
MODEL_SAVE_PATH = 'machine_learning/creating_model/chess_evaluation_model.joblib'
TEST_SIZE = 0.2
RANDOM_STATE = 42

def parse_feature_vector(vector_string):
    parsed_tuple = ast.literal_eval(vector_string)
    return list(parsed_tuple)

print(f"Loading data from '{CSV_FILE_PATH}'...")
df = pd.read_csv(CSV_FILE_PATH, delimiter=';', converters={'FeatureVector': parse_feature_vector})
df.dropna(subset=['FeatureVector', 'Evaluation'], inplace=True)
print(f"Data loaded successfully. Found {len(df)} valid rows.")

print("\nPreparing data for the model...")
X = np.array(df['FeatureVector'].tolist())
y = df['Evaluation'].values

print(f"Features (X) shape: {X.shape}")
print(f"Target (y) shape: {y.shape}")

print("\nSplitting data into training and testing sets...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
)
print(f"Training set size: {len(X_train)}")
print(f"Testing set size: {len(X_test)}")

print("\nInitializing and training the RandomForestRegressor model...")
model = RandomForestRegressor(n_estimators=100, random_state=RANDOM_STATE, n_jobs=-1, oob_score=True)

model.fit(X_train, y_train)

if hasattr(model, 'oob_score_'):
    print(f"Model Out-of-Bag (OOB) Score: {model.oob_score_:.4f}")

print("Model training complete.")

print("\nEvaluating the model on the test set...")
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
print(f"R-squared (R²) Score: {r2:.4f}")

print(f"\nSaving the trained model to '{MODEL_SAVE_PATH}'...")
try:
    joblib.dump(model, MODEL_SAVE_PATH)
    print("Model saved successfully.")
except Exception as e:
    print(f"Error saving the model: {e}")

print("\nScript finished.")
