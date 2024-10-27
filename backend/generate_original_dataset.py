from chess import get_fresh_game_state, execute_move
import random
from tqdm import tqdm
from stockfish import Stockfish
import csv
from train_model import train_model

stockfish = Stockfish(path='/opt/homebrew/bin/stockfish')

feature_vector_to_evaluation = {}

desired_num_rows_of_data = int(1e4)
num_games = int(desired_num_rows_of_data / 74.9)
print(f'Running {num_games} random chess games of maximum 80 halfmoves and collecting and having Stockfish give an evaluation for every position achieved (should be around {desired_num_rows_of_data})...')
for i in tqdm(range(num_games)):
    game_state = get_fresh_game_state()
    while game_state['status'] == 'live' and game_state['move_number'] != 41:
        stockfish.set_FEN_position(game_state['FEN'])
        evaluation = stockfish.get_evaluation()
        if evaluation['type'] == 'cp':
            feature_vector_to_evaluation[tuple(game_state['feature_vector'])] = evaluation['value']
        execute_move(random.choice(tuple(game_state['legal_moves'])), game_state)

with open('backend/original_dataset.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Feature_Vector', 'Evaluation'])
    for feature_vector, evaluation in feature_vector_to_evaluation.items():
        writer.writerow([feature_vector, evaluation])

train_model()
