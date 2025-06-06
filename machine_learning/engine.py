import sys
sys.path.append('')
from chess import executeMove, BLACK
from copy import deepcopy
import joblib
import numpy as np

loaded_model = joblib.load('machine_learning/creating_model/chess_evaluation_model.joblib')

def modelPredict(feature_vector):
    return loaded_model.predict(feature_vector)


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
