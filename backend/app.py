from chess import getFreshGameState, executeMove
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
from copy import deepcopy

app = Flask(__name__)
CORS(app)

model = joblib.load('backend/chess_position_evaluator.pkl')

gameState = getFreshGameState()
square_selected = None
move_suggestions = None
square_suggestions = None

def get_evaluation_at_depth(depth, gameState):
    if not depth:
        return model.predict(np.array(gameState['featureVector']).reshape(1, -1))
    move_to_eval = {}
    for move in gameState['legalMoves']:
        gameState_copy = deepcopy(gameState)
        executeMove(move, gameState_copy)
        move_to_eval[move] = model.predict(np.array(gameState_copy['featureVector']).reshape(1, -1))
    if gameState['featureVector'][64] == 1:
        executeMove(max(move_to_eval, key=move_to_eval.get), gameState)
    else:
        executeMove(min(move_to_eval, key=move_to_eval.get), gameState)
    return get_evaluation_at_depth(depth - 1, gameState)

@app.route('/api/square-clicked', methods=['POST'])
def square_clicked():
    global gameState
    global square_selected
    global move_suggestions
    global square_suggestions
    move_executed = False
    square_clicked = (request.get_json().get('row_index'), request.get_json().get('col_index'))
    if square_selected:
        for move_suggestion in move_suggestions:
            if move_suggestion[1] == square_clicked:
                executeMove(move_suggestion, gameState)
                square_selected = None
                move_suggestions = None
                square_suggestions = None
                move_executed = True
                # if len(gameState['legalMoves']) != 0:
                #     move_to_eval = {}
                #     for move in gameState['legalMoves']:
                #         gameState_copy = deepcopy(gameState)
                #         executeMove(move, gameState_copy)
                #         move_to_eval[move] = get_evaluation_at_depth(0, gameState_copy)
                #     executeMove(min(move_to_eval, key=move_to_eval.get), gameState)
                break
    if not move_executed and square_clicked in [move[0] for move in gameState['legalMoves']]:
        square_selected = square_clicked
        move_suggestions = [move for move in gameState['legalMoves'] if move[0] == square_selected]
        square_suggestions = [move[1] for move in move_suggestions]
    else:
        square_selected = None
        move_suggestions = None
        square_suggestions = None
    return jsonify({
        'board-vector': gameState['featureVector'][:64],
        'selected-square': square_selected,
        'square-suggestions': square_suggestions,
        'status': gameState['status']
    })

if __name__ == '__main__':
    app.run(debug=True)
