import pandas as pd
from tqdm import tqdm
import numpy as np
import ast
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from time import time
import joblib
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

NUMBER_OF_ROWS_OF_DATA_TO_TRAIN_ON = 6_000_000

print('Reading \'dataset.csv\' file...')
df = pd.read_csv('backend/dataset.csv', sep=';', nrows=NUMBER_OF_ROWS_OF_DATA_TO_TRAIN_ON)

tqdm.pandas()

print('Loading the feature vectors...')
X = np.array(df['Feature_Vector'].progress_apply(ast.literal_eval).tolist())
y = df['Evaluation'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=18, max_depth=61, n_jobs=-1, random_state=42, verbose=3) # Sweet spot: n_estimators=18, max_depth=61

start_time = time()
print('Training...')
model.fit(X_train, y_train)
joblib.dump(model, 'backend/chess_position_evaluator.pkl')
print(f'Training time: {(time() - start_time):.4f} seconds')

y_pred = model.predict(X_test)

print(f'R²: {r2_score(y_test, y_pred):.4f}\nMAE: {mean_absolute_error(y_test, y_pred):.4f}')

# Matplotlib visualizations:
plt.figure(figsize=(8, 8))
plt.xticks(np.arange(-900, 901, 150))
plt.yticks(np.arange(-900, 901, 150))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([-900, 900], [-900, 900], color='red', linestyle='--')
plt.xlabel('Actual Evaluation')
plt.ylabel('Predicted Evaluation')
plt.title('Predicted vs Actual Evaluation')
plt.show()
