from chess import getFreshGameState, LIVE, executeMove
import random
from tqdm import tqdm


def simulateRandomGameCappedAt79Halfmoves():
    gameState = getFreshGameState()
    for i in range(79):
        if gameState['status'] != LIVE:
            break
        executeMove(random.choice(gameState['legalMoves']), gameState)

def simulateRandomGamesCappedAt79Halfmoves(numberOfGames):
    for i in tqdm(range(numberOfGames)):
        simulateRandomGameCappedAt79Halfmoves()


def simulateRandomGame():
    gameState = getFreshGameState()
    numberOfHalfmoves = 0
    while gameState['status'] == LIVE:
        executeMove(random.choice(gameState['legalMoves']), gameState)
        numberOfHalfmoves += 1
    return numberOfHalfmoves

def simulateRandomGames(numberOfGames):
    totalNumberOfHalfmoves = 0
    for i in tqdm(range(numberOfGames)):
        totalNumberOfHalfmoves += simulateRandomGame()
    averageNumberOfHalfmoves = totalNumberOfHalfmoves / numberOfGames
    return averageNumberOfHalfmoves



numberOfGames = 30
averageNumberOfHalfmoves = simulateRandomGames(numberOfGames)

print(f"Average number of halfmoves from {numberOfGames} games: {averageNumberOfHalfmoves}")

# "Average number of halfmoves from 3000 games: 341"


# The average number of halfmoves of a completely random chess game might be about 340.



# Consider collecting data like stats about each individual piece (how
# many moves it makes, how long it survives, what typically captures it)
