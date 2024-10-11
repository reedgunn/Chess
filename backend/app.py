from chess_logic import fresh_game_state, execute_move, execute_move_just_for_checking_legality, piece_legal_moves, is_color, legal_moves
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import joblib
import numpy as np
from copy import deepcopy

def game_state_to_feature_vector(board, active_color, castling_rights, en_passant_square):
    return [square for row in board for square in row] + active_color + castling_rights + en_passant_square

app = Flask(__name__)
CORS(app)

model = joblib.load('chess_position_evaluator.pkl')

game_state = fresh_game_state()
selected_square = []
square_suggestions = []

@app.route('/api/square-clicked', methods=['POST'])
def square_clicked():
    global game_state
    global selected_square
    global square_suggestions
    square_clicked = [request.get_json().get('row_index'), request.get_json().get('col_index')]
    if square_clicked in square_suggestions:
        execute_move([selected_square, square_clicked], game_state)
        if len(game_state['legal_moves']) != 0:
            move_to_eval = {}
            for move in game_state['legal_moves']:
                game_state_copy = deepcopy(game_state)
                execute_move_just_for_checking_legality(move, game_state_copy['board'], game_state_copy['active_color'], game_state_copy['castling_rights'], game_state_copy['en_passant_square'], game_state_copy['pieces'])
                move_to_eval[tuple([tuple(pos) for pos in move])] = model.predict(np.array(game_state_to_feature_vector(game_state_copy['board'], game_state_copy['active_color'], game_state_copy['castling_rights'], game_state_copy['en_passant_square'])).reshape(1, -1))
            execute_move(min(move_to_eval, key=move_to_eval.get), game_state)
            if len(game_state['legal_moves']) != 0:
                selected_square = []
                square_suggestions = []
    elif is_color(game_state['active_color'][0], square_clicked, game_state['board']) and len([piece_legal_move[1] for piece_legal_move in piece_legal_moves(square_clicked, game_state['board'], game_state['active_color'], game_state['castling_rights'], game_state['en_passant_square'], game_state['pieces'])]) > 0:
        selected_square = square_clicked
        square_suggestions = [piece_legal_move[1] for piece_legal_move in piece_legal_moves(square_clicked, game_state['board'], game_state['active_color'], game_state['castling_rights'], game_state['en_passant_square'], game_state['pieces'])]
    else:
        selected_square = []
        square_suggestions = []
    return jsonify({
        'selected-square': selected_square,
        'square-suggestions': square_suggestions,
        'board-matrix': game_state['board'],
        'status': game_state['status']
    })

@app.route('/api/get-board-state', methods=['GET'])
def get_board_state():
    global game_state
    global selected_square
    global square_suggestions
    return jsonify({
        'selected-square': selected_square,
        'square-suggestions': square_suggestions,
        'board-matrix': game_state['board'],
        'status': game_state['status']
    })

if __name__ == '__main__':
    app.run(debug=True)