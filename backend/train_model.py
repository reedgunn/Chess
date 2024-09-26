import pandas as pd
import numpy as np
import ast
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib
from time import time

start_time = time()
df = pd.read_csv('chessData_processed.csv')

X = pd.DataFrame(df['Feature_Vector'].apply(ast.literal_eval).tolist())
y = df['Evaluation']

X_train, X_test, y_train, y_test = train_test_split(X, y)
model = RandomForestRegressor()
model.fit(X_train, y_train)
joblib.dump(model, 'chess_position_evaluator.pkl')

y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)

print(f'Mean Absolute Error: {mae:.2f}')
print(f'Time elapsed: {(time() - start_time):.1f}')