from chess import getFreshGameState, executeMove, encodedStatusToStatus, BLACK
from flask import Flask, request, jsonify
from flask_cors import CORS
from copy import deepcopy
import torch
import torch.nn as nn
import torch.nn.functional as F

class ChessEvaluator(nn.Module):
    def __init__(self, input_size):
        super(ChessEvaluator, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
model = ChessEvaluator(71)
device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
model.to(device)
model_path = 'backend/machine_learning/chess_evaluator_state_dict.pth'
model.load_state_dict(torch.load(model_path, map_location=device))
model.eval()
def modelPredict(feature_vector):
    with torch.no_grad():
        input_tensor = torch.tensor(feature_vector, dtype=torch.float32).unsqueeze(0).to(device)
        output = model(input_tensor)
        evaluation = output.item()
    return evaluation

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

def getImprovedEvaluation(depth, gameState):
    if not depth:
        return modelPredict(gameState['featureVector'])
    availableMoveToEvaluation = {}
    for move in gameState['legalMoves']:
        gameStateCopy = deepcopy(gameState)
        executeMove(move, gameStateCopy)
        availableMoveToEvaluation[move] = modelPredict(gameStateCopy['featureVector'])
    if gameState['featureVector'][64] == BLACK:
        executeMove(min(availableMoveToEvaluation, key=availableMoveToEvaluation.get), gameState)
    else:
        executeMove(max(availableMoveToEvaluation, key=availableMoveToEvaluation.get), gameState)
    return getImprovedEvaluation(depth - 1, gameState)

def executeEngineMove(depth, gameState, whoseTurnItIs):
    availableMoveToEvaluation = {}
    for move in gameState['legalMoves']:
        gameStateCopy = deepcopy(gameState)
        executeMove(move, gameStateCopy)
        availableMoveToEvaluation[move] = getImprovedEvaluation(depth, gameStateCopy)
    if whoseTurnItIs == BLACK:
        executeMove(min(availableMoveToEvaluation, key=availableMoveToEvaluation.get), gameState)
    else:
        executeMove(max(availableMoveToEvaluation, key=availableMoveToEvaluation.get), gameState)

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