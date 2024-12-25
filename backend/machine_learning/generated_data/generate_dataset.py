import sys
sys.path.append('backend/python_backend')
from chess import getFreshGameState, executeMove, LIVE
import random
from tqdm import tqdm
from stockfish import Stockfish
import csv
from time import time

stockfishDepth = 7
stockfish = Stockfish(path='/opt/homebrew/bin/stockfish', depth=stockfishDepth)

featureVectorToEvaluation = {}

def simulateRandomGame(featureVectorToEvaluation, maximumNumberOfHalfmoves):
    gameState = getFreshGameState()
    for i in range(maximumNumberOfHalfmoves):
        if gameState['status'] != LIVE:
            break
        stockfish.set_fen_position(gameState['FEN'])
        evaluation = stockfish.get_evaluation()
        featureVectorToEvaluation[tuple(gameState['featureVector'])] = evaluation['value']
        executeMove(random.choice(gameState['legalMoves']), gameState)

def simulateRandomGames(numberOfGames, featureVectorToEvaluation, maximumNumberOfHalfmoves):
    for i in tqdm(range(numberOfGames)):
        simulateRandomGame(featureVectorToEvaluation, maximumNumberOfHalfmoves)

numberOfGames = 10
maximumNumberOfHalfmoves = 114
print(f"Running {numberOfGames} random chess games cut off at {maximumNumberOfHalfmoves} halfmoves and collecting and having Stockfish give an evaluation at depth {stockfishDepth} for every position achieved...")
simulateRandomGames(numberOfGames, featureVectorToEvaluation, maximumNumberOfHalfmoves)

with open('backend/machine_learning/generated_data/generated_dataset.csv', mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['FeatureVector', 'Evaluation'])
    for featureVector, evaluation in featureVectorToEvaluation.items():
        writer.writerow([featureVector, evaluation])