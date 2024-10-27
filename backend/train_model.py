import pandas as pd

print('Reading \'dataset.csv\' file...')
df = pd.read_csv('backend/dataset.csv', sep=';')

import numpy as np
from tqdm import tqdm
tqdm.pandas()
import ast

print('Reading feature vectors...')
X = np.array(df['Feature_Vector'].progress_apply(ast.literal_eval).tolist())
y = df['Evaluation'].values

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor(n_estimators=22, max_depth=62, n_jobs=-1, random_state=42, verbose=3) # Sweet spot: n_estimators=22, max_depth=62, 

from time import time
import joblib

start_time = time()
print('Training...')
model.fit(X_train, y_train)
joblib.dump(model, 'backend/chess_position_evaluator.pkl')
print(f'Training time: {(time() - start_time):.5f} seconds')

y_pred = model.predict(X_test)

from sklearn.metrics import mean_absolute_error
print(f'Mean absolute error: {mean_absolute_error(y_test, y_pred)}')

import matplotlib.pyplot as plt
plt.figure(figsize=(8, 8))
plt.xticks(np.arange(-900, 901, 150))
plt.yticks(np.arange(-900, 901, 150))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([-900, 900], [-900, 900], color='red', linestyle='--')
plt.xlabel('Actual Evaluation')
plt.ylabel('Predicted Evaluation')
plt.title('Predicted vs Actual Evaluation')
plt.show()
