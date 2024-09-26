import pandas as pd
from tqdm import tqdm

FEN_piece_to_int_piece = {
    'P': 1, 'R': 2, 'N': 3, 'B': 4, 'Q': 5, 'K': 6,
    'p': -1, 'r': -2, 'n': -3, 'b': -4, 'q': -5, 'k': -6
}
def FEN_board_to_encoded_list(FEN_board):
    res = [0] * 64
    i = 0
    for c in FEN_board:
        if c.isdigit():
            i += int(c)
        elif c != '/':
            res[i] = FEN_piece_to_int_piece[c]
            i += 1
    return res

def FEN_active_color_to_encoded_list(FEN_active_color):
    return [1] if FEN_active_color == 'w' else [-1]

FEN_castling_rights_char_to_index = {
    'K': 0, 'Q': 1, 'k': 2, 'q': 3
}
def FEN_castling_rights_to_encoded_list(FEN_castling_rights):
    res = [0, 0, 0, 0]
    if FEN_castling_rights != '-':
        for c in FEN_castling_rights:
            res[FEN_castling_rights_char_to_index[c]] = 1
    return res

def FEN_en_passant_square_to_encoded_list(FEN_en_passant_square):
    if FEN_en_passant_square == '-':
        return [-1, -1]
    return [abs(8 - int(FEN_en_passant_square[1])), ord(FEN_en_passant_square[0]) - 97]

def FEN_to_feature_vector(FEN):
    FEN_board, FEN_active_color, FEN_castling_rights, FEN_en_passant_square = FEN.split(' ', 4)[:4]
    board_encoded = FEN_board_to_encoded_list(FEN_board)
    active_color_encoded = FEN_active_color_to_encoded_list(FEN_active_color)
    castling_rights_encoded = FEN_castling_rights_to_encoded_list(FEN_castling_rights)
    en_passant_square_encoded = FEN_en_passant_square_to_encoded_list(FEN_en_passant_square)
    return board_encoded + active_color_encoded + castling_rights_encoded + en_passant_square_encoded

def string_evaluation_to_int(string_evaluation):
    if string_evaluation[0] == '#':
        if string_evaluation[1] == '-':
            return -328
        else:
            return 328
    return int(string_evaluation)

tqdm.pandas()

chunk_size = 100000

with pd.read_csv('chessData.csv', chunksize=chunk_size) as reader:
    for i, chunk in tqdm(enumerate(reader)):
        chunk['Feature_Vector'] = chunk['FEN'].apply(FEN_to_feature_vector)
        chunk['Evaluation'] = chunk['Evaluation'].apply(string_evaluation_to_int)
        chunk = chunk.drop(columns=['FEN'])
        mode = 'w' if i == 0 else 'a'
        chunk.to_csv('chessData_processed.csv', mode=mode, header=(i == 0), index=False)