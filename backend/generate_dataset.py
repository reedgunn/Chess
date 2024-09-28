from chess_logic import fresh_game_state, execute_move, legal_moves
import random
from tqdm import tqdm
from stockfish import Stockfish
import csv

# rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

# Feature vector: for training machine learning models
# Game state: dictionary of lists for handling state of game and executing moves, etc.
# FEN: standard format for sending chess positions to APIs, etc.

# Need: game_state_to_FEN() and game_state_to_feature_vector()

FEN_cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
FEN_rows = ['8', '7', '6', '5', '4', '3', '2', '1']
int_piece_to_FEN_piece = {
    1: 'P', 2: 'R', 3: 'N', 4: 'B', 5: 'Q', 6: 'K',
    -1: 'p', -2: 'r', -3: 'n', -4: 'b', -5: 'q', -6: 'k',
}
def game_state_to_FEN(board, active_color, castling_rights, en_passant_square, halfmoves_since_last_pawn_move_or_capture):
    res = ''
    count = 0
    for row in board:
        for square in row:
            if square == 0:
                count += 1
            else:
                if count > 0:
                    res += str(count)
                    count = 0
                res += int_piece_to_FEN_piece[square]
        if count > 0:
            res += str(count)
            count = 0
        res += '/'
    res = res[:-1]
    if active_color[0] == 1:
        res += ' w'
    else:
        res += ' b'
    if castling_rights == [0, 0, 0, 0]:
        res += ' -'
    else:
        res += ' '
        castling_rights_ = ['K', 'Q', 'k', 'q']
        for i in range(4):
            if castling_rights[i]:
                res += castling_rights_[i]
    if en_passant_square == [-1, -1]:
        res += ' -'
    else:
        res += ' ' + FEN_cols[en_passant_square[1]] + FEN_rows[en_passant_square[0]]
    res += ' ' + str(game_state['halfmoves_since_last_pawn_move_or_capture'][0])
    res += ' 1'
    return res


depth = 5
stockfish = Stockfish(path='/opt/homebrew/bin/stockfish', depth=depth)

feature_vector_to_evaluation = {}

num_rows_of_data = 2e6
num_games = int(num_rows_of_data / 75)
for i in tqdm(range(num_games), f'Running {num_games} random chess games, collecting and having Stockfish give an evaluation at depth {depth} for every position achieved'):
    game_state = fresh_game_state()
    num_halfmoves = 0
    while game_state['status'][0] == 'live' and num_halfmoves < 79:
        FEN = game_state_to_FEN(game_state['board'], game_state['active_color'], game_state['castling_rights'], game_state['en_passant_square'], game_state['halfmoves_since_last_pawn_move_or_capture'])
        stockfish.set_fen_position(FEN)
        evaluation = stockfish.get_evaluation()['value']
        # print(f'{FEN} -> {evaluation}')
        feature_vector_to_evaluation[tuple(game_state['past_positions'][-1])] = evaluation
        move_to_execute = random.choice(game_state['legal_moves'])
        execute_move(move_to_execute, game_state)
        num_halfmoves += 1

with open('dataset.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Feature_Vector', 'Evaluation'])
    for feature_vector, evaluation in feature_vector_to_evaluation.items():
        writer.writerow([feature_vector, evaluation])

print(len(feature_vector_to_evaluation))
