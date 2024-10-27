import pandas as pd

print('Reading the imported .csv file...')
df = pd.read_csv('backend/imported_dataset.csv', nrows=7.2e6)

EVALUATION_MAGNITUDE_THRESHOLD = 901

def should_keep(evaluation):
    first_char = evaluation[0]
    if first_char == '#' or first_char == '0':
        return False
    return int(evaluation[1:]) < EVALUATION_MAGNITUDE_THRESHOLD

from tqdm import tqdm
tqdm.pandas()

print(f'Removing all rows of data where the evaluation is a draw or checkmate, or has magnitude of at least {EVALUATION_MAGNITUDE_THRESHOLD}...')
df = df[df['Evaluation'].progress_apply(should_keep)]

print('Removing the plus sign from the positive evaluations...')
df['Evaluation'] = df['Evaluation'].progress_apply(lambda x : x[1:] if x[0] == '+' else x)

FEN_piece_to_int_piece = {
    'P': 1, 'R': 2, 'N': 3, 'B': 4, 'Q': 5, 'K': 6,
    'p': -1, 'r': -2, 'n': -3, 'b': -4, 'q': -5, 'k': -6
}
FEN_row_to_row_index = {
    '1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0
}
FEN_col_to_col_index = {
    'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7
}
def FEN_to_feature_vector(FEN):
    res = [0] * 71
    board, active_color, castling_rights, en_passant_square = FEN.split()[:4]
    i = 0
    for c in board:
        if c != '/':
            if c.isdigit():
                i += int(c)
            else:
                res[i] = FEN_piece_to_int_piece[c]
                i += 1
    res[64] = 1 if active_color == 'w' else -1
    res[65] = 1 if 'K' in castling_rights else 0
    res[66] = 1 if 'Q' in castling_rights else 0
    res[67] = 1 if 'k' in castling_rights else 0
    res[68] = 1 if 'q' in castling_rights else 0
    if en_passant_square != '-':
        res[69] = FEN_row_to_row_index[en_passant_square[1]]
        res[70] = FEN_col_to_col_index[en_passant_square[0]]
    else:
        res[69], res[70] = -1, -1
    return res

print('Converting the FENs into feature vectors...')
df['FEN'] = df['FEN'].progress_apply(FEN_to_feature_vector)
df.rename(columns={'FEN': 'Feature_Vector'}, inplace=True)

print('Exporting data to \'dataset.csv\'...')
df.to_csv('backend/dataset.csv', sep=';', index=False)
