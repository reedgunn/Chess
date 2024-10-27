from chess import get_fresh_game_state, execute_move
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
from copy import deepcopy

ENGINE_DEPTH = 3

app = Flask(__name__)
CORS(app)

model = joblib.load('backend/chess_position_evaluator.pkl')

game_state = get_fresh_game_state()
square_selected = None
move_suggestions = None
square_suggestions = None

def get_evaluation_at_depth(depth, game_state):
    if not depth:
        return model.predict(np.array(game_state['feature_vector']).reshape(1, -1))
    move_to_eval = {}
    for move in game_state['legal_moves']:
        game_state_copy = deepcopy(game_state)
        execute_move(move, game_state_copy)
        move_to_eval[move] = model.predict(np.array(game_state_copy['feature_vector']).reshape(1, -1))
    if game_state['feature_vector'][64] == 1:
        execute_move(max(move_to_eval, key=move_to_eval.get), game_state)
    else:
        execute_move(min(move_to_eval, key=move_to_eval.get), game_state)
    return get_evaluation_at_depth(depth - 1, game_state)

@app.route('/api/square-clicked', methods=['POST'])
def square_clicked():
    global game_state
    global square_selected
    global move_suggestions
    global square_suggestions
    move_executed = False
    square_clicked = (request.get_json().get('row_index'), request.get_json().get('col_index'))
    if square_selected:
        for move_suggestion in move_suggestions:
            if move_suggestion[1] == square_clicked:
                execute_move(move_suggestion, game_state)
                square_selected = None
                move_suggestions = None
                square_suggestions = None
                move_executed = True
                if len(game_state['legal_moves']) != 0:
                    move_to_eval = {}
                    for move in game_state['legal_moves']:
                        game_state_copy = deepcopy(game_state)
                        execute_move(move, game_state_copy)
                        move_to_eval[move] = get_evaluation_at_depth(ENGINE_DEPTH - 1, game_state_copy)
                    execute_move(min(move_to_eval, key=move_to_eval.get), game_state)
                break
    if not move_executed and square_clicked in [move[0] for move in game_state['legal_moves']]:
        square_selected = square_clicked
        move_suggestions = [move for move in game_state['legal_moves'] if move[0] == square_selected]
        square_suggestions = [move[1] for move in move_suggestions]
    else:
        square_selected = None
        move_suggestions = None
        square_suggestions = None
    return jsonify({
        'board-vector': game_state['feature_vector'][:64],
        'selected-square': square_selected,
        'square-suggestions': square_suggestions,
        'status': game_state['status']
    })

if __name__ == '__main__':
    app.run(debug=True)
