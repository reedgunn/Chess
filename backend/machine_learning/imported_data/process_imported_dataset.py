import sys
sys.path.append('backend/python_backend')
from chess import FENToFeatureVector

import pandas as pd
from tqdm import tqdm

print('Reading the imported .csv file...')
df = pd.read_csv('backend/machine_learning/imported_data/chessData.csv', nrows=100)

tqdm.pandas()

print(f'Removing all rows of data where the evaluation is a checkmate...')
df = df[df['Evaluation'].progress_apply(lambda x: x[0] != '#')]

print('Removing the plus sign from the positive evaluations...')
df['Evaluation'] = df['Evaluation'].progress_apply(lambda x : x[1:] if x[0] == '+' else x)

print('Converting the FENs into feature vectors...')
df['FEN'] = df['FEN'].progress_apply(FENToFeatureVector)
df.rename(columns={'FEN': 'FeatureVector'}, inplace=True)

print('Exporting data to \'processed_imported_dataset.csv\'...')
df.to_csv('backend/machine_learning/imported_data/processed_imported_dataset.csv', sep=';', index=False)