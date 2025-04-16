import sys
sys.path.append('')
from chess import getFreshGameState, executeMove, encodedStatusToStatus, BLACK
sys.path.append('machine_learning')
from engine import executeEngineMove
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

gameState = getFreshGameState()
selectedSquare = None
suggestedSquares = None

def setLegalMovesInitialPositionsToFinalPositionsToMoves(gameState):
    res = dict()
    for move in gameState['legalMoves']:
        if move[0] not in res:
            res[move[0]] = dict()
        res[move[0]][move[1]] = move
    return res

legalMovesInitialPositionsToFinalPositionsToMoves = setLegalMovesInitialPositionsToFinalPositionsToMoves(gameState)

DEPTH = 3

@app.route('/api/squareClicked', methods=['POST'])
def squareClicked():
    global gameState
    global selectedSquare
    global suggestedSquares
    global legalMovesInitialPositionsToFinalPositionsToMoves

    clickedSquare = (request.get_json().get('rowIndex'), request.get_json().get('columnIndex'))

    if clickedSquare in legalMovesInitialPositionsToFinalPositionsToMoves:
        selectedSquare = clickedSquare
        suggestedSquares = [finalPosition for finalPosition in legalMovesInitialPositionsToFinalPositionsToMoves[selectedSquare]]
    else:
        if selectedSquare and clickedSquare in suggestedSquares:
            executeMove(legalMovesInitialPositionsToFinalPositionsToMoves[selectedSquare][clickedSquare], gameState)
            executeEngineMove(DEPTH, gameState, BLACK)
            legalMovesInitialPositionsToFinalPositionsToMoves = setLegalMovesInitialPositionsToFinalPositionsToMoves(gameState)
        selectedSquare = None
        suggestedSquares = None
    return jsonify({
        'board': gameState['featureVector'][:64],
        'selectedSquare': selectedSquare,
        'suggestedSquares': suggestedSquares,
        'status': encodedStatusToStatus[gameState['status']]
    })

app.run(debug=True)