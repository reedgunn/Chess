import chess
from collections import defaultdict
import random
from tqdm import tqdm
import time

symbols = {
    6: ' ', 5: '♟', 1: '♞', 2: '♝', 0: '♜', 3: '♛', 4: '♚', 
    7: '♙', 9: '♘', 10: '♗', 8: '♖', 11: '♕', 12: '♔'
}
def displayBoard(featureVector):
    boardMatrix = [[0] * 8 for i in range(8)]
    for i in range(64):
        boardMatrix[i // 8][i % 8] = symbols[featureVector[i]]
    print(' --- --- --- --- --- --- --- --- ')
    for i in range(8):
        print('| ' + ' '.join(map(lambda x : f'{x} |', boardMatrix[i])))
        print(' --- --- --- --- --- --- --- --- ')

def runGames(numGames):
    results = defaultdict(int)
    for i in tqdm(range(numGames)):
        gameState = chess.getFreshGameState()
        while True:
            # print(gameState['FEN'])
            # displayBoard(gameState['featureVector'])
            # time.sleep(1.5)
            chess.executeMove(random.choice(tuple(gameState['legalMoves'])), gameState)
            if gameState['status'] != chess.LIVE:
                # displayBoard(gameState['featureVector'])
                # print(gameState['status'])
                results[gameState['status']] += 1
                break
    for key, value in results.items():
        print(f'{key}: {value}')



def simulateRandomGame():
    gameState = chess.getFreshGameState()
    while gameState['status'] == chess.LIVE:
        chess.executeMove(random.choice(gameState['legalMoves']), gameState)

def simulateRandomGames(numberOfGames):
    for i in tqdm(range(numberOfGames)):
        simulateRandomGame()


def simulateRandomGameCappedAt79Halfmoves():
    gameState = chess.getFreshGameState()
    for i in range(79):
        if gameState['status'] != chess.LIVE:
            break
        chess.executeMove(random.choice(gameState['legalMoves']), gameState)

def simulateRandomGamesCappedAt79Halfmoves(numberOfGames):
    for i in tqdm(range(numberOfGames)):
        simulateRandomGameCappedAt79Halfmoves()


simulateRandomGames(50)

simulateRandomGamesCappedAt79Halfmoves(50)