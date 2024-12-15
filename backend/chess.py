from collections import defaultdict
from pyrsistent import freeze
import random
from tqdm import tqdm
import time

intPieceToFenPieceBlack = {-1: 'p', -2: 'r', -3: 'n', -4: 'b', -5: 'q', -6: 'k'}
intPieceToFenPieceWhite = {1: 'P', 2: 'R', 3: 'N', 4: 'B', 5: 'Q', 6: 'K'}
fenCastlingRightsBlack = ('k', 'q')
fenCastlingRightsWhite = ('K', 'Q')
fenColumns = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
fenRows = ('8', '7', '6', '5', '4', '3', '2', '1')
def gameStateToFen(currentPosition, halfmovesSinceLastCaptureOrPawnMove, moveNumber):
    Fen = ''
    for i in range(8):
        emptySquaresCount = 0
        for j in range(8):
            position = (i, j)
            if position not in currentPosition['pieces'][-1] and position not in currentPosition['pieces'][1]:
                emptySquaresCount += 1
            else:
                if emptySquaresCount:
                    Fen += str(emptySquaresCount)
                    emptySquaresCount = 0
                if position in currentPosition['pieces'][-1]:
                    Fen += intPieceToFenPieceBlack[currentPosition['pieces'][-1][position]]
                else:
                    Fen += intPieceToFenPieceWhite[currentPosition['pieces'][1][position]]
        if emptySquaresCount:
            Fen += str(emptySquaresCount)
        if i != 7:
            Fen += '/'
    Fen += ' w ' if currentPosition['activeColor'] == 1 else ' b '
    castlingRights = ''
    for i in range(2):
        if currentPosition['castlingRights'][1][i]:
            castlingRights += fenCastlingRightsWhite[i]
    for i in range(2):
        if currentPosition['castlingRights'][-1][i]:
            castlingRights += fenCastlingRightsBlack[i]
    Fen += castlingRights + ' ' if castlingRights else '- '
    Fen += fenColumns[currentPosition['enPassantSquare'][1]] + fenRows[currentPosition['enPassantSquare'][0]] + ' ' if currentPosition['enPassantSquare'] else '- '
    Fen += str(halfmovesSinceLastCaptureOrPawnMove) + ' ' + str(moveNumber)
    return Fen

def getFreshGameState():
    gameState = {}
    gameState['currentPosition'] = {
        'pieces': {
            -1: {
                (0, 0): -2, (0, 1): -3, (0, 2): -4, (0, 3): -5, (0, 4): -6, (0, 5): -4, (0, 6): -3, (0, 7): -2,
                (1, 0): -1, (1, 1): -1, (1, 2): -1, (1, 3): -1, (1, 4): -1, (1, 5): -1, (1, 6): -1, (1, 7): -1
            },
            1: {
                (6, 0):  1, (6, 1):  1, (6, 2):  1, (6, 3):  1, (6, 4):  1, (6, 5):  1, (6, 6):  1, (6, 7):  1,
                (7, 0):  2, (7, 1):  3, (7, 2):  4, (7, 3):  5, (7, 4):  6, (7, 5):  4, (7, 6):  3, (7, 7):  2
            }
        },
        'activeColor': 1,
        'castlingRights': {-1: [1, 1], 1: [1, 1]},
        'enPassantSquare': None
    }
    gameState['kingPositions'] = {-1: (0, 4), 1: (7, 4)}
    gameState['positionsSinceLastCaptureOrPawnMove'] = defaultdict(int, {freeze(gameState['currentPosition']): 1})
    gameState['halfmovesSinceLastCaptureOrPawnMove'] = 0
    gameState['legalMoves'] = legalMoves(gameState['currentPosition'], gameState['kingPositions'][gameState['currentPosition']['activeColor']])
    gameState['status'] = 'live'
    return gameState

def getFreshGameState_trackingFeatureVector():
    gameState = {}
    gameState['currentPosition'] = {
        'pieces': {
            -1: {
                (0, 0): -2, (0, 1): -3, (0, 2): -4, (0, 3): -5, (0, 4): -6, (0, 5): -4, (0, 6): -3, (0, 7): -2,
                (1, 0): -1, (1, 1): -1, (1, 2): -1, (1, 3): -1, (1, 4): -1, (1, 5): -1, (1, 6): -1, (1, 7): -1
            },
            1: {
                (6, 0):  1, (6, 1):  1, (6, 2):  1, (6, 3):  1, (6, 4):  1, (6, 5):  1, (6, 6):  1, (6, 7):  1,
                (7, 0):  2, (7, 1):  3, (7, 2):  4, (7, 3):  5, (7, 4):  6, (7, 5):  4, (7, 6):  3, (7, 7):  2
            }
        },
        'activeColor': 1,
        'castlingRights': {-1: [1, 1], 1: [1, 1]},
        'enPassantSquare': None
    }
    gameState['kingPositions'] = {-1: (0, 4), 1: (7, 4)}
    gameState['positionsSinceLastCaptureOrPawnMove'] = defaultdict(int, {freeze(gameState['currentPosition']): 1})
    gameState['halfmovesSinceLastCaptureOrPawnMove'] = 0
    gameState['legalMoves'] = legalMoves(gameState['currentPosition'], gameState['kingPositions'][gameState['currentPosition']['activeColor']])
    gameState['status'] = 'live'
    gameState['featureVector'] = [-2, -3, -4, -5, -6, -4, -3, -2, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 6, 4, 3, 2, 1, 1, 1, 1, 1, -1, -1]
    return gameState

def getFreshGameState_trackingFeatureVector_trackingFen():
    gameState = {}
    gameState['currentPosition'] = {
        'pieces': {
            -1: {
                (0, 0): -2, (0, 1): -3, (0, 2): -4, (0, 3): -5, (0, 4): -6, (0, 5): -4, (0, 6): -3, (0, 7): -2,
                (1, 0): -1, (1, 1): -1, (1, 2): -1, (1, 3): -1, (1, 4): -1, (1, 5): -1, (1, 6): -1, (1, 7): -1
            },
            1: {
                (6, 0):  1, (6, 1):  1, (6, 2):  1, (6, 3):  1, (6, 4):  1, (6, 5):  1, (6, 6):  1, (6, 7):  1,
                (7, 0):  2, (7, 1):  3, (7, 2):  4, (7, 3):  5, (7, 4):  6, (7, 5):  4, (7, 6):  3, (7, 7):  2
            }
        },
        'activeColor': 1,
        'castlingRights': {-1: [1, 1], 1: [1, 1]},
        'enPassantSquare': None
    }
    gameState['kingPositions'] = {-1: (0, 4), 1: (7, 4)}
    gameState['positionsSinceLastCaptureOrPawnMove'] = defaultdict(int, {freeze(gameState['currentPosition']): 1})
    gameState['halfmovesSinceLastCaptureOrPawnMove'] = 0
    gameState['legalMoves'] = legalMoves(gameState['currentPosition'], gameState['kingPositions'][gameState['currentPosition']['activeColor']])
    gameState['status'] = 'live'
    gameState['featureVector'] = [-2, -3, -4, -5, -6, -4, -3, -2, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 6, 4, 3, 2, 1, 1, 1, 1, 1, -1, -1]
    gameState['moveNumber'] = 1
    gameState['Fen'] = gameStateToFen(gameState['currentPosition'], gameState['halfmovesSinceLastCaptureOrPawnMove'], gameState['moveNumber'])
    return gameState

def isEmpty(pos, pieces):
    return pos not in pieces[-1] and pos not in pieces[1]

def squaresThreatenedByPawn(pos, color):
    res = set()
    finalRowIndex, initialColumnIndex = pos[0] - color, pos[1]
    if initialColumnIndex != 0:
        res.add((finalRowIndex, initialColumnIndex - 1))
    if initialColumnIndex != 7:
        res.add((finalRowIndex, initialColumnIndex + 1))
    return res

def squaresThreatenedByRook(pos, pieces):
    res = set()
    rowIndex, columnIndex = pos
    # Sliding north:
    curPos = [rowIndex - 1, columnIndex]
    while curPos[0] != -1:
        addition = tuple(curPos)
        res.add(addition)
        if not isEmpty(addition, pieces):
            break
        curPos[0] -= 1
    # Sliding east:
    curPos = [rowIndex, columnIndex + 1]
    while curPos[1] != 8:
        addition = tuple(curPos)
        res.add(addition)
        if not isEmpty(addition, pieces):
            break
        curPos[1] += 1
    # Sliding south:
    curPos = [rowIndex + 1, columnIndex]
    while curPos[0] != 8:
        addition = tuple(curPos)
        res.add(addition)
        if not isEmpty(addition, pieces):
            break
        curPos[0] += 1
    # Sliding west:
    curPos = [rowIndex, columnIndex - 1]
    while curPos[1] != -1:
        addition = tuple(curPos)
        res.add(addition)
        if not isEmpty(addition, pieces):
            break
        curPos[1] -= 1
    #
    return res

def squaresThreatenedByKnight(pos):
    res = set()
    rowIndex, columnIndex = pos
    notOnTopEdge = rowIndex != 0
    notCloseToTopEdge = notOnTopEdge and rowIndex != 1
    notOnRightEdge = columnIndex != 7
    notCloseToRightEdge = notOnRightEdge and columnIndex != 6
    notOnBottomEdge = rowIndex != 7
    notCloseToBottomEdge = notOnBottomEdge and rowIndex != 6
    notOnLeftEdge = columnIndex != 0
    notCloseToLeftEdge = notOnLeftEdge and columnIndex != 1
    # Big up
    if notCloseToTopEdge:
        finalRowIndex = rowIndex - 2
        # Small left
        if notOnLeftEdge:
            res.add((finalRowIndex, columnIndex - 1))
        # Small right
        if notOnRightEdge:
            res.add((finalRowIndex, columnIndex + 1))
    # Big right
    if notCloseToRightEdge:
        finalColumnIndex = columnIndex + 2
        # Small up
        if notOnTopEdge:
            res.add((rowIndex - 1, finalColumnIndex))
        # Small down
        if notOnBottomEdge:
            res.add((rowIndex + 1, finalColumnIndex))
    # Big down
    if notCloseToBottomEdge:
        finalRowIndex = rowIndex + 2
        # Small right
        if notOnRightEdge:
            res.add((finalRowIndex, columnIndex + 1))
        # Small left
        if notOnLeftEdge:
            res.add((finalRowIndex, columnIndex - 1))
    # Big left
    if notCloseToLeftEdge:
        finalColumnIndex = columnIndex - 2
        # Small down
        if notOnBottomEdge:
            res.add((rowIndex + 1, finalColumnIndex))
        # Small up
        if notOnTopEdge:
            res.add((rowIndex - 1, finalColumnIndex))
    #
    return res

def squaresThreatenedByBishop(pos, pieces):
    res = set()
    rowIndex, columnIndex = pos
    # Sliding northeast:
    curPos = [rowIndex - 1, columnIndex + 1]
    while curPos[0] != -1 and curPos[1] != 8:
        addition = tuple(curPos)
        res.add(addition)
        if not isEmpty(addition, pieces):
            break
        curPos[0] -= 1
        curPos[1] += 1
    # Sliding southeast:
    curPos = [rowIndex + 1, columnIndex + 1]
    while curPos[0] != 8 and curPos[1] != 8:
        addition = tuple(curPos)
        res.add(addition)
        if not isEmpty(addition, pieces):
            break
        curPos[0] += 1
        curPos[1] += 1
    # Sliding southwest:
    curPos = [rowIndex + 1, columnIndex - 1]
    while curPos[0] != 8 and curPos[1] != -1:
        addition = tuple(curPos)
        res.add(addition)
        if not isEmpty(addition, pieces):
            break
        curPos[0] += 1
        curPos[1] -= 1
    # Sliding northwest:
    curPos = [rowIndex - 1, columnIndex - 1]
    while curPos[0] != -1 and curPos[1] != -1:
        addition = tuple(curPos)
        res.add(addition)
        if not isEmpty(addition, pieces):
            break
        curPos[0] -= 1
        curPos[1] -= 1
    #
    return res

def squaresThreatenedByQueen(pos, pieces):
    return squaresThreatenedByRook(pos, pieces) | squaresThreatenedByBishop(pos, pieces)

def squaresThreatenedByKing(pos):
    res = set()
    rowIndex, columnIndex = pos
    notOnTopEdge = rowIndex != 0
    notOnRightEdge = columnIndex != 7
    notOnBottomEdge = rowIndex != 7
    notOnLeftEdge = columnIndex != 0
    # North:
    if notOnTopEdge:
        finalRowIndex = rowIndex - 1
        # Northwest:
        if notOnLeftEdge:
            res.add((finalRowIndex, columnIndex - 1))
        # North:
        res.add((finalRowIndex, columnIndex))
        # Northeast:
        if notOnRightEdge:
            res.add((finalRowIndex, columnIndex + 1))
    # South:
    if notOnBottomEdge:
        finalRowIndex = rowIndex + 1
        # Southwest:
        if notOnLeftEdge:
            res.add((finalRowIndex, columnIndex - 1))
        # South:
            res.add((finalRowIndex, columnIndex))
        # Southeast:
        if notOnRightEdge:
            res.add((finalRowIndex, columnIndex + 1))
    # West:
    if notOnLeftEdge:
        res.add((rowIndex, columnIndex - 1))
    # East:
    if notOnRightEdge:
        res.add((rowIndex, columnIndex + 1))
    #
    return res

def squaresThreatenedByColor(color, pieces):
    res = set()
    for pos, piece in pieces[color].items():
        pieceType = piece * color
        if pieceType == 1:
            res.update(squaresThreatenedByPawn(pos, color))
        elif pieceType == 2:
            res.update(squaresThreatenedByRook(pos, pieces))
        elif pieceType == 3:
            res.update(squaresThreatenedByKnight(pos))
        elif pieceType == 4:
            res.update(squaresThreatenedByBishop(pos, pieces))
        elif pieceType == 5:
            res.update(squaresThreatenedByQueen(pos, pieces))
        else:
            res.update(squaresThreatenedByKing(pos))
    return res

def isColorInCheck(color, kingPosition, pieces):
    return kingPosition in squaresThreatenedByColor(color * -1, pieces)

# move vector: (initialPosition, finalPosition, positionOfCapturedPiece (or None if move isn't a capture))

def doesMoveLeaveKingInCheck(move, color, kingPosition, pieces):
    initialPosition, finalPosition, positionOfCapturedPiece = move
    oppositeColor = color * -1
    pieces[color][finalPosition] = pieces[color].pop(initialPosition)
    capturedPiece = pieces[oppositeColor].pop(positionOfCapturedPiece) if positionOfCapturedPiece else None
    res = isColorInCheck(color, kingPosition, pieces)
    if capturedPiece:
        pieces[oppositeColor][positionOfCapturedPiece] = capturedPiece
    pieces[color][initialPosition] = pieces[color].pop(finalPosition)
    return res
    
def addMoveToResIfDoesntLeaveKingInCheck(res, move, color, kingPosition, pieces):
    if not doesMoveLeaveKingInCheck(move, color, kingPosition, pieces):
        res.add(move)
    
def pawnLegalMoves(pos, color, kingPosition, pieces, enPassantSquare):
    res = set()
    rowIndex, columnIndex = pos
    doubleJumpRowIndex = 1 if color == -1 else 6
    oppositeColor = color * -1
    singleHopFinalPosition = (rowIndex - color, columnIndex)
    if isEmpty(singleHopFinalPosition, pieces):
        addMoveToResIfDoesntLeaveKingInCheck(res, (pos, singleHopFinalPosition, None), color, kingPosition, pieces)
        if rowIndex == doubleJumpRowIndex:
            doubleHopFinalPosition = (singleHopFinalPosition[0] - color, columnIndex)
            if isEmpty(doubleHopFinalPosition, pieces):
                addMoveToResIfDoesntLeaveKingInCheck(res, (pos, doubleHopFinalPosition, None), color, kingPosition, pieces)
    if columnIndex != 0:
        leftCaptureFinalPosition = (singleHopFinalPosition[0], columnIndex - 1)
        if leftCaptureFinalPosition in pieces[oppositeColor]:
            addMoveToResIfDoesntLeaveKingInCheck(res, (pos, leftCaptureFinalPosition, leftCaptureFinalPosition), color, kingPosition, pieces)
        elif leftCaptureFinalPosition == enPassantSquare:
            addMoveToResIfDoesntLeaveKingInCheck(res, (pos, leftCaptureFinalPosition, (rowIndex, leftCaptureFinalPosition[1])), color, kingPosition, pieces)
    if columnIndex != 7:
        rightCaptureFinalPosition = (singleHopFinalPosition[0], columnIndex + 1)
        if rightCaptureFinalPosition in pieces[oppositeColor]:
            addMoveToResIfDoesntLeaveKingInCheck(res, (pos, rightCaptureFinalPosition, rightCaptureFinalPosition), color, kingPosition, pieces)
        elif rightCaptureFinalPosition == enPassantSquare:
            addMoveToResIfDoesntLeaveKingInCheck(res, (pos, rightCaptureFinalPosition, (rowIndex, rightCaptureFinalPosition[1])), color, kingPosition, pieces)
    return res

def rookLegalMoves(pos, color, pieces, kingPosition):
    res = set()
    rowIndex, columnIndex = pos
    oppositeColor = color * -1
    # Sliding north:
    curPos = (rowIndex - 1, columnIndex)
    while curPos[0] != -1 and curPos not in pieces[color]:
        if curPos in pieces[oppositeColor]:
            addMoveToResIfDoesntLeaveKingInCheck(res, (pos, curPos, curPos), color, kingPosition, pieces)
            break
        addMoveToResIfDoesntLeaveKingInCheck(res, (pos, curPos, None), color, kingPosition, pieces)
        curPos = (curPos[0] - 1, columnIndex)
    # Sliding east:
    curPos = (rowIndex, columnIndex + 1)
    while curPos[1] != 8 and curPos not in pieces[color]:
        if curPos in pieces[oppositeColor]:
            addMoveToResIfDoesntLeaveKingInCheck(res, (pos, curPos, curPos), color, kingPosition, pieces)
            break
        addMoveToResIfDoesntLeaveKingInCheck(res, (pos, curPos, None), color, kingPosition, pieces)
        curPos = (rowIndex, curPos[1] + 1)
    # Sliding south:
    curPos = (rowIndex + 1, columnIndex)
    while curPos[0] != 8 and curPos not in pieces[color]:
        if curPos in pieces[oppositeColor]:
            addMoveToResIfDoesntLeaveKingInCheck(res, (pos, curPos, curPos), color, kingPosition, pieces)
            break
        addMoveToResIfDoesntLeaveKingInCheck(res, (pos, curPos, None), color, kingPosition, pieces)
        curPos = (curPos[0] + 1, columnIndex)
    # Sliding west:
    curPos = (rowIndex, columnIndex - 1)
    while curPos[1] != -1 and curPos not in pieces[color]:
        if curPos in pieces[oppositeColor]:
            addMoveToResIfDoesntLeaveKingInCheck(res, (pos, curPos, curPos), color, kingPosition, pieces)
            break
        addMoveToResIfDoesntLeaveKingInCheck(res, (pos, curPos, None), color, kingPosition, pieces)
        curPos = (rowIndex, curPos[1] - 1)
    #
    return res

def helper(res, possibleFinalPosition, initialPosition, color, kingPosition, pieces):
    if possibleFinalPosition not in pieces[color]:
        if possibleFinalPosition in pieces[color * -1]:
            addMoveToResIfDoesntLeaveKingInCheck(res, (initialPosition, possibleFinalPosition, possibleFinalPosition), color, kingPosition, pieces)
        else:
            addMoveToResIfDoesntLeaveKingInCheck(res, (initialPosition, possibleFinalPosition, None), color, kingPosition, pieces)

def knightLegalMoves(pos, color, kingPosition, pieces):
    res = set()
    rowIndex, columnIndex = pos
    notOnTopEdge = rowIndex != 0
    notCloseToTopEdge = notOnTopEdge and rowIndex != 1
    notOnRightEdge = columnIndex != 7
    notCloseToRightEdge = notOnRightEdge and columnIndex != 6
    notOnBottomEdge = rowIndex != 7
    notCloseToBottomEdge = notOnBottomEdge and rowIndex != 6
    notOnLeftEdge = columnIndex != 0
    notCloseToLeftEdge = notOnLeftEdge and columnIndex != 1
    # Big up
    if notCloseToTopEdge:
        finalRowIndex = rowIndex - 2
        # Small left
        if notOnLeftEdge:
            helper(res, (finalRowIndex, columnIndex - 1), pos, color, kingPosition, pieces)
        # Small right
        if notOnRightEdge:
            helper(res, (finalRowIndex, columnIndex + 1), pos, color, kingPosition, pieces)
    # Big right
    if notCloseToRightEdge:
        finalColumnIndex = columnIndex + 2
        # Small up
        if notOnTopEdge:
            helper(res, (rowIndex - 1, finalColumnIndex), pos, color, kingPosition, pieces)
        # Small down
        if notOnBottomEdge:
            helper(res, (rowIndex + 1, finalColumnIndex), pos, color, kingPosition, pieces)
    # Big down
    if notCloseToBottomEdge:
        finalRowIndex = rowIndex + 2
        # Small right
        if notOnRightEdge:
            helper(res, (finalRowIndex, columnIndex + 1), pos, color, kingPosition, pieces)
        # Small left
        if notOnLeftEdge:
            helper(res, (finalRowIndex, columnIndex - 1), pos, color, kingPosition, pieces)
    # Big left
    if notCloseToLeftEdge:
        finalColumnIndex = columnIndex - 2
        # Small down
        if notOnBottomEdge:
            helper(res, (rowIndex + 1, finalColumnIndex), pos, color, kingPosition, pieces)
        # Small up
        if notOnTopEdge:
            helper(res, (rowIndex - 1, finalColumnIndex), pos, color, kingPosition, pieces)
    #
    return res

def bishopLegalMoves(pos, color, pieces, kingPosition):
    res = set()
    rowIndex, columnIndex = pos
    oppositeColor = color * -1
    # Sliding northeast:
    curPos = (rowIndex - 1, columnIndex + 1)
    while curPos[0] != -1 and curPos[1] != 8 and curPos not in pieces[color]:
        if curPos in pieces[oppositeColor]:
            addMoveToResIfDoesntLeaveKingInCheck(res, (pos, curPos, curPos), color, kingPosition, pieces)
            break
        addMoveToResIfDoesntLeaveKingInCheck(res, (pos, curPos, None), color, kingPosition, pieces)
        curPos = (curPos[0] - 1, curPos[1] + 1)
    # Sliding southeast:
    curPos = (rowIndex + 1, columnIndex + 1)
    while curPos[0] != 8 and curPos[1] != 8 and curPos not in pieces[color]:
        if curPos in pieces[oppositeColor]:
            addMoveToResIfDoesntLeaveKingInCheck(res, (pos, curPos, curPos), color, kingPosition, pieces)
            break
        addMoveToResIfDoesntLeaveKingInCheck(res, (pos, curPos, None), color, kingPosition, pieces)
        curPos = (curPos[0] + 1, curPos[1] + 1)
    # Sliding southwest:
    curPos = (rowIndex + 1, columnIndex - 1)
    while curPos[0] != 8 and curPos[1] != -1 and curPos not in pieces[color]:
        if curPos in pieces[oppositeColor]:
            addMoveToResIfDoesntLeaveKingInCheck(res, (pos, curPos, curPos), color, kingPosition, pieces)
            break
        addMoveToResIfDoesntLeaveKingInCheck(res, (pos, curPos, None), color, kingPosition, pieces)
        curPos = (curPos[0] + 1, curPos[1] - 1)
    # Sliding northwest:
    curPos = (rowIndex - 1, columnIndex - 1)
    while curPos[0] != -1 and curPos[1] != -1 and curPos not in pieces[color]:
        if curPos in pieces[oppositeColor]:
            addMoveToResIfDoesntLeaveKingInCheck(res, (pos, curPos, curPos), color, kingPosition, pieces)
            break
        addMoveToResIfDoesntLeaveKingInCheck(res, (pos, curPos, None), color, kingPosition, pieces)
        curPos = (curPos[0] - 1, curPos[1] - 1)
    #
    return res

def queenLegalMoves(pos, color, pieces, kingPosition):
    return rookLegalMoves(pos, color, pieces, kingPosition) | bishopLegalMoves(pos, color, pieces, kingPosition)

def kingLegalMoves(pos, color, pieces, castlingRights):
    res = set()
    rowIndex, columnIndex = pos
    notOnTopEdge = rowIndex != 0
    notOnRightEdge = columnIndex != 7
    notOnBottomEdge = rowIndex != 7
    notOnLeftEdge = columnIndex != 0
    # North:
    if notOnTopEdge:
        finalRowIndex = rowIndex - 1
        # Northwest:
        if notOnLeftEdge:
            finalPosition = (finalRowIndex, columnIndex - 1)
            helper(res, finalPosition, pos, color, finalPosition, pieces)
        # North:
        finalPosition = (finalRowIndex, columnIndex)
        helper(res, finalPosition, pos, color, finalPosition, pieces)
        # Northeast:
        if notOnRightEdge:
            finalPosition = (finalRowIndex, columnIndex + 1)
            helper(res, finalPosition, pos, color, finalPosition, pieces)
    # South:
    if notOnBottomEdge:
        finalRowIndex = rowIndex + 1
        # Southwest:
        if notOnLeftEdge:
            finalPosition = (finalRowIndex, columnIndex - 1)
            helper(res, finalPosition, pos, color, finalPosition, pieces)
        # South:
        finalPosition = (finalRowIndex, columnIndex)
        helper(res, finalPosition, pos, color, finalPosition, pieces)
        # Southeast:
        if notOnRightEdge:
            finalPosition = (finalRowIndex, columnIndex + 1)
            helper(res, finalPosition, pos, color, finalPosition, pieces)
    # West:
    if notOnLeftEdge:
        finalPosition = (rowIndex, columnIndex - 1)
        helper(res, finalPosition, pos, color, finalPosition, pieces)
    # East:
    if notOnRightEdge:
        finalPosition = (rowIndex, columnIndex + 1)
        helper(res, finalPosition, pos, color, finalPosition, pieces)
    #
    squaresThreatenedByOpponent = squaresThreatenedByColor(color * -1, pieces)
    if pos not in squaresThreatenedByOpponent:
        castlingRowIndex = 0 if color == -1 else 7
        if castlingRights[0]:
            squareOneToRightOfKing = (castlingRowIndex, 5)
            if isEmpty(squareOneToRightOfKing, pieces) and squareOneToRightOfKing not in squaresThreatenedByOpponent:
                squareTwoToRightOfKing = (castlingRowIndex, 6)
                if isEmpty(squareTwoToRightOfKing, pieces) and squareTwoToRightOfKing not in squaresThreatenedByOpponent:
                    res.add((pos, squareTwoToRightOfKing, None))
        if castlingRights[1]:
            squareOneToLeftOfKing = (castlingRowIndex, 3)
            if isEmpty(squareOneToLeftOfKing, pieces) and squareOneToLeftOfKing not in squaresThreatenedByOpponent:
                squareTwoToLeftOfKing = (castlingRowIndex, 2)
                if isEmpty(squareTwoToLeftOfKing, pieces) and squareTwoToLeftOfKing not in squaresThreatenedByOpponent and isEmpty((castlingRowIndex, 1), pieces):
                    res.add((pos, squareTwoToLeftOfKing, None))
    return res

def legalMoves(currentPosition, kingPosition):
    res = set()
    for pos, piece in currentPosition['pieces'][currentPosition['activeColor']].copy().items():
        pieceType = piece * currentPosition['activeColor']
        if pieceType == 1:
            res.update(pawnLegalMoves(pos, currentPosition['activeColor'], kingPosition, currentPosition['pieces'], currentPosition['enPassantSquare']))
        elif pieceType == 2:
            res.update(rookLegalMoves(pos, currentPosition['activeColor'], currentPosition['pieces'], kingPosition))
        elif pieceType == 3:
            res.update(knightLegalMoves(pos, currentPosition['activeColor'], kingPosition, currentPosition['pieces']))
        elif pieceType == 4:
            res.update(bishopLegalMoves(pos, currentPosition['activeColor'], currentPosition['pieces'], kingPosition))
        elif pieceType == 5:
            res.update(queenLegalMoves(pos, currentPosition['activeColor'], currentPosition['pieces'], kingPosition))
        else:
            res.update(kingLegalMoves(pos, currentPosition['activeColor'], currentPosition['pieces'], currentPosition['castlingRights'][currentPosition['activeColor']]))
    return res

def executeMove(move, gameState):
    initialPosition, finalPosition, positionOfCapturedPiece = move
    if gameState['currentPosition']['activeColor'] == -1:
        color = -1
        oppositeColor = 1
        queen = -5
        rook = -2
        king = -6
        promotionRowIndex = 7
        castlingRowIndex = 0
        opponentCastlingRowIndex = 7
        pawnDoubleJumpInitialRowIndex = 1
        pawnDoubleJumpFinalRowIndex = 3
        newEnPassantSquareRowIndex = 2
    else:
        color = 1
        oppositeColor = -1
        queen = 5
        rook = 2
        king = 6
        promotionRowIndex = 0
        castlingRowIndex = 7
        opponentCastlingRowIndex = 0
        pawnDoubleJumpInitialRowIndex = 6
        pawnDoubleJumpFinalRowIndex = 4
        newEnPassantSquareRowIndex = 5
        
    whatIsMoving = gameState['currentPosition']['pieces'][color][initialPosition]

    # Changing halfmovesSinceLastCaptureOrPawnMove: If the move is a capture or a pawn move, set to 0, otherwise increment by 1
    if positionOfCapturedPiece or whatIsMoving == color:
        gameState['halfmovesSinceLastCaptureOrPawnMove'] = 0
        gameState['positionsSinceLastCaptureOrPawnMove'] = defaultdict(int)
    else:
        if gameState['halfmovesSinceLastCaptureOrPawnMove'] == 99:
            gameState['status'] = 'Draw by 50-move-rule'
            return
        gameState['halfmovesSinceLastCaptureOrPawnMove'] += 1

    # Changing board state: special cases = [castling, pawn promotion, en passant], default = move the piece
    if whatIsMoving == king:
        gameState['kingPositions'][color] = finalPosition
        if move == ((castlingRowIndex, 4), (castlingRowIndex, 6), None):
            gameState['currentPosition']['pieces'][color].pop((castlingRowIndex, 7))
            gameState['currentPosition']['pieces'][color][(castlingRowIndex, 5)] = rook
        elif move == ((castlingRowIndex, 4), (castlingRowIndex, 2), None):
            gameState['currentPosition']['pieces'][color].pop((castlingRowIndex, 0))
            gameState['currentPosition']['pieces'][color][(castlingRowIndex, 3)] = rook
    if positionOfCapturedPiece:
        gameState['currentPosition']['pieces'][oppositeColor].pop(positionOfCapturedPiece)
    gameState['currentPosition']['pieces'][color].pop(initialPosition)
    if whatIsMoving == color and finalPosition[0] == promotionRowIndex:
        gameState['currentPosition']['pieces'][color][finalPosition] = queen
    else:
        gameState['currentPosition']['pieces'][color][finalPosition] = whatIsMoving

    # Changing castling rights: if you move your king or one of your rooks for the first time, or if you capture one of your opponents rooks
    if initialPosition == (castlingRowIndex, 4):
        if gameState['currentPosition']['castlingRights'][color][0]:
            gameState['currentPosition']['castlingRights'][color][0] = 0
        if gameState['currentPosition']['castlingRights'][color][1]:
            gameState['currentPosition']['castlingRights'][color][1] = 0
    elif initialPosition == (castlingRowIndex, 7) and gameState['currentPosition']['castlingRights'][color][0]:
        gameState['currentPosition']['castlingRights'][color][0] = 0
    elif initialPosition == (castlingRowIndex, 0) and gameState['currentPosition']['castlingRights'][color][1]:
        gameState['currentPosition']['castlingRights'][color][1] = 0
    if finalPosition == (opponentCastlingRowIndex, 0) and gameState['currentPosition']['castlingRights'][oppositeColor][1]:
        gameState['currentPosition']['castlingRights'][oppositeColor][1] = 0
    elif finalPosition == (opponentCastlingRowIndex, 7) and gameState['currentPosition']['castlingRights'][oppositeColor][0]:
        gameState['currentPosition']['castlingRights'][oppositeColor][0] = 0
    
    # Changing en passant square: If your move is a pawn double-jump, set the en passant square accordingly, else set it to None
    if whatIsMoving == color and initialPosition[0] == pawnDoubleJumpInitialRowIndex and finalPosition[0] == pawnDoubleJumpFinalRowIndex:
        gameState['currentPosition']['enPassantSquare'] = (newEnPassantSquareRowIndex, finalPosition[1])
    else:
        gameState['currentPosition']['enPassantSquare'] = None

    # Check for draw by threefold repetition:
    # "Two positions are by definition 'the same' if the same types of pieces occupy the same squares, the same player 
    # has the move, the remaining castling rights are the same and the possibility to capture en passant is the same."
    position = freeze(gameState['currentPosition'])
    if gameState['positionsSinceLastCaptureOrPawnMove'][position] == 2:
        gameState['status'] = 'Draw by threefold repetition'
        return
    else:
        gameState['positionsSinceLastCaptureOrPawnMove'][position] += 1

    # Check for draw by insufficient material:
    numWhitePieces = len(gameState['currentPosition']['pieces'][1])
    numBlackPieces = len(gameState['currentPosition']['pieces'][-1])
    numPieces = numWhitePieces + numBlackPieces
    if numWhitePieces == 2 and 4 in gameState['currentPosition']['pieces'][1].values() and numBlackPieces == 2 and -4 in gameState['currentPosition']['pieces'][-1].values():
        for pos, piece in gameState['currentPosition']['pieces'][1].items():
            if piece == 4:
                whiteBishopPos = pos
                break
        for pos, piece in gameState['currentPosition']['pieces'][-1].items():
            if piece == -4:
                blackBishopPos = pos
                break
        if (whiteBishopPos[0] + whiteBishopPos[1]) % 2 == (blackBishopPos[0] + blackBishopPos[1]) % 2:
            gameState['status'] = 'Draw by insufficient material (king and bishop versus king and bishop with the bishops on the same color)'
            return
    elif numPieces == 3:
        if numWhitePieces == 2:
            whitePieces = gameState['currentPosition']['pieces'][1].values()
            if 3 in whitePieces:
                gameState['status'] = 'Draw by insufficient material (king and knight versus king)'
                return
            if 4 in whitePieces:
                gameState['status'] = 'Draw by insufficient material (king and bishop versus king)'
                return
        else:
            blackPieces = gameState['currentPosition']['pieces'][-1].values()
            if -3 in blackPieces:
                gameState['status'] = 'Draw by insufficient material (king and knight versus king)'
                return
            if -4 in blackPieces:
                gameState['status'] = 'Draw by insufficient material (king and bishop versus king)'
                return
    elif numPieces == 2:
        gameState['status'] = 'Draw by insufficient material (king versus king)'
        return

    # Always change the active color to the opposite of what it currently is
    gameState['currentPosition']['activeColor'] *= -1

    gameState['legalMoves'] = legalMoves(gameState['currentPosition'], gameState['kingPositions'][gameState['currentPosition']['activeColor']])

    if not len(gameState['legalMoves']):
        if isColorInCheck(gameState['currentPosition']['activeColor'], gameState['kingPositions'][gameState['currentPosition']['activeColor']], gameState['currentPosition']['pieces']):
            if color == 1:
                gameState['status'] = 'White checkmates black'
            else:
                gameState['status'] = 'Black checkmates white'
        else:
            if color == 1:
                gameState['status'] = 'White stalemates black'
            else:
                gameState['status'] = 'Black stalemates white'
        return

def executeMove_trackingFeatureVector(move, gameState):
    initialPosition, finalPosition, positionOfCapturedPiece = move
    if gameState['currentPosition']['activeColor'] == -1:
        color = -1
        oppositeColor = 1
        queen = -5
        rook = -2
        king = -6
        promotionRowIndex = 7
        castlingRowIndex = 0
        opponentCastlingRowIndex = 7
        pawnDoubleJumpInitialRowIndex = 1
        pawnDoubleJumpFinalRowIndex = 3
        newEnPassantSquareRowIndex = 2
        kingsideCastlingRightFeatureVectorIndex = 67
        queensideCastlingRightFeatureVectorIndex = 68
    else:
        color = 1
        oppositeColor = -1
        queen = 5
        rook = 2
        king = 6
        promotionRowIndex = 0
        castlingRowIndex = 7
        opponentCastlingRowIndex = 0
        pawnDoubleJumpInitialRowIndex = 6
        pawnDoubleJumpFinalRowIndex = 4
        newEnPassantSquareRowIndex = 5
        kingsideCastlingRightFeatureVectorIndex = 65
        queensideCastlingRightFeatureVectorIndex = 66
        
    whatIsMoving = gameState['currentPosition']['pieces'][color][initialPosition]

    # Changing halfmovesSinceLastCaptureOrPawnMove: If the move is a capture or a pawn move, set to 0, otherwise increment by 1
    if positionOfCapturedPiece or whatIsMoving == color:
        gameState['halfmovesSinceLastCaptureOrPawnMove'] = 0
        gameState['positionsSinceLastCaptureOrPawnMove'] = defaultdict(int)
    else:
        if gameState['halfmovesSinceLastCaptureOrPawnMove'] == 99:
            gameState['status'] = 'Draw by 50-move-rule'
            return
        gameState['halfmovesSinceLastCaptureOrPawnMove'] += 1

    # Changing board state: special cases = [castling, pawn promotion, en passant], default = move the piece
    if whatIsMoving == king:
        gameState['kingPositions'][color] = finalPosition
        if move == ((castlingRowIndex, 4), (castlingRowIndex, 6), None):
            gameState['currentPosition']['pieces'][color].pop((castlingRowIndex, 7))
            gameState['currentPosition']['pieces'][color][(castlingRowIndex, 5)] = rook
            gameState['featureVector'][castlingRowIndex * 8 + 7] = 0
            gameState['featureVector'][castlingRowIndex * 8 + 5] = rook
        elif move == ((castlingRowIndex, 4), (castlingRowIndex, 2), None):
            gameState['currentPosition']['pieces'][color].pop((castlingRowIndex, 0))
            gameState['currentPosition']['pieces'][color][(castlingRowIndex, 3)] = rook
            gameState['featureVector'][castlingRowIndex * 8] = 0
            gameState['featureVector'][castlingRowIndex * 8 + 3] = rook
    if positionOfCapturedPiece:
        gameState['currentPosition']['pieces'][oppositeColor].pop(positionOfCapturedPiece)
        gameState['featureVector'][positionOfCapturedPiece[0] * 8 + positionOfCapturedPiece[1]] = 0
    gameState['currentPosition']['pieces'][color].pop(initialPosition)
    gameState['featureVector'][initialPosition[0] * 8 + initialPosition[1]] = 0
    if whatIsMoving == color and finalPosition[0] == promotionRowIndex:
        gameState['currentPosition']['pieces'][color][finalPosition] = queen
        gameState['featureVector'][finalPosition[0] * 8 + finalPosition[1]] = queen
    else:
        gameState['currentPosition']['pieces'][color][finalPosition] = whatIsMoving
        gameState['featureVector'][finalPosition[0] * 8 + finalPosition[1]] = whatIsMoving

    # Changing castling rights: if you move your king or one of your rooks for the first time, or if you capture one of your opponents rooks
    if initialPosition == (castlingRowIndex, 4):
        if gameState['currentPosition']['castlingRights'][color][0]:
            gameState['currentPosition']['castlingRights'][color][0] = 0
            gameState['featureVector'][kingsideCastlingRightFeatureVectorIndex] = 0
        if gameState['currentPosition']['castlingRights'][color][1]:
            gameState['currentPosition']['castlingRights'][color][1] = 0
            gameState['featureVector'][queensideCastlingRightFeatureVectorIndex] = 0
    elif initialPosition == (castlingRowIndex, 7) and gameState['currentPosition']['castlingRights'][color][0]:
        gameState['currentPosition']['castlingRights'][color][0] = 0
        gameState['featureVector'][kingsideCastlingRightFeatureVectorIndex] = 0
    elif initialPosition == (castlingRowIndex, 0) and gameState['currentPosition']['castlingRights'][color][1]:
        gameState['currentPosition']['castlingRights'][color][1] = 0
        gameState['featureVector'][queensideCastlingRightFeatureVectorIndex] = 0
    if finalPosition == (opponentCastlingRowIndex, 0) and gameState['currentPosition']['castlingRights'][oppositeColor][1]:
        gameState['currentPosition']['castlingRights'][oppositeColor][1] = 0
        gameState['featureVector'][queensideCastlingRightFeatureVectorIndex] = 0
    elif finalPosition == (opponentCastlingRowIndex, 7) and gameState['currentPosition']['castlingRights'][oppositeColor][0]:
        gameState['currentPosition']['castlingRights'][oppositeColor][0] = 0
        gameState['featureVector'][kingsideCastlingRightFeatureVectorIndex] = 0
    
    # Changing en passant square: If your move is a pawn double-jump, set the en passant square accordingly, else set it to None
    if whatIsMoving == color and initialPosition[0] == pawnDoubleJumpInitialRowIndex and finalPosition[0] == pawnDoubleJumpFinalRowIndex:
        gameState['currentPosition']['enPassantSquare'] = (newEnPassantSquareRowIndex, finalPosition[1])
        gameState['featureVector'][69], gameState['featureVector'][70] = newEnPassantSquareRowIndex, finalPosition[1]
    else:
        gameState['currentPosition']['enPassantSquare'] = None
        gameState['featureVector'][69], gameState['featureVector'][70] = -1, -1

    
    # Check for draw by threefold repetition:
    # "Two positions are by definition 'the same' if the same types of pieces occupy the same squares, the same player 
    # has the move, the remaining castling rights are the same and the possibility to capture en passant is the same."
    position = freeze(gameState['currentPosition'])
    if gameState['positionsSinceLastCaptureOrPawnMove'][position] == 2:
        gameState['status'] = 'Draw by threefold repetition'
        return
    else:
        gameState['positionsSinceLastCaptureOrPawnMove'][position] += 1

    # Check for draw by insufficient material:
    numWhitePieces = len(gameState['currentPosition']['pieces'][1])
    numBlackPieces = len(gameState['currentPosition']['pieces'][-1])
    numPieces = numWhitePieces + numBlackPieces
    if numWhitePieces == 2 and 4 in gameState['currentPosition']['pieces'][1].values() and numBlackPieces == 2 and -4 in gameState['currentPosition']['pieces'][-1].values():
        for pos, piece in gameState['currentPosition']['pieces'][1].items():
            if piece == 4:
                whiteBishopPos = pos
                break
        for pos, piece in gameState['currentPosition']['pieces'][-1].items():
            if piece == -4:
                blackBishopPos = pos
                break
        if (whiteBishopPos[0] + whiteBishopPos[1]) % 2 == (blackBishopPos[0] + blackBishopPos[1]) % 2:
            gameState['status'] = 'Draw by insufficient material (king and bishop versus king and bishop with the bishops on the same color)'
            return
    elif numPieces == 3:
        if numWhitePieces == 2:
            whitePieces = gameState['currentPosition']['pieces'][1].values()
            if 3 in whitePieces:
                gameState['status'] = 'Draw by insufficient material (king and knight versus king)'
                return
            if 4 in whitePieces:
                gameState['status'] = 'Draw by insufficient material (king and bishop versus king)'
                return
        else:
            blackPieces = gameState['currentPosition']['pieces'][-1].values()
            if -3 in blackPieces:
                gameState['status'] = 'Draw by insufficient material (king and knight versus king)'
                return
            if -4 in blackPieces:
                gameState['status'] = 'Draw by insufficient material (king and bishop versus king)'
                return
    elif numPieces == 2:
        gameState['status'] = 'Draw by insufficient material (king versus king)'
        return

    # Always change the active color to the opposite of what it currently is
    gameState['currentPosition']['activeColor'] *= -1
    gameState['featureVector'][64] *= -1

    gameState['legalMoves'] = legalMoves(gameState['currentPosition'], gameState['kingPositions'][gameState['currentPosition']['activeColor']])

    if not len(gameState['legalMoves']):
        if isColorInCheck(gameState['currentPosition']['activeColor'], gameState['kingPositions'][gameState['currentPosition']['activeColor']], gameState['currentPosition']['pieces']):
            if color == 1:
                gameState['status'] = 'White checkmates black'
            else:
                gameState['status'] = 'Black checkmates white'
        else:
            if color == 1:
                gameState['status'] = 'White stalemates black'
            else:
                gameState['status'] = 'Black stalemates white'
        return

def executeMove_trackingFeatureVector_trackingFen(move, gameState):
    initialPosition, finalPosition, positionOfCapturedPiece = move
    if gameState['currentPosition']['activeColor'] == -1:
        color = -1
        oppositeColor = 1
        queen = -5
        rook = -2
        king = -6
        promotionRowIndex = 7
        castlingRowIndex = 0
        opponentCastlingRowIndex = 7
        pawnDoubleJumpInitialRowIndex = 1
        pawnDoubleJumpFinalRowIndex = 3
        newEnPassantSquareRowIndex = 2
        kingsideCastlingRightFeatureVectorIndex = 67
        queensideCastlingRightFeatureVectorIndex = 68
    else:
        color = 1
        oppositeColor = -1
        queen = 5
        rook = 2
        king = 6
        promotionRowIndex = 0
        castlingRowIndex = 7
        opponentCastlingRowIndex = 0
        pawnDoubleJumpInitialRowIndex = 6
        pawnDoubleJumpFinalRowIndex = 4
        newEnPassantSquareRowIndex = 5
        kingsideCastlingRightFeatureVectorIndex = 65
        queensideCastlingRightFeatureVectorIndex = 66
        
    whatIsMoving = gameState['currentPosition']['pieces'][color][initialPosition]

    # Changing halfmovesSinceLastCaptureOrPawnMove: If the move is a capture or a pawn move, set to 0, otherwise increment by 1
    if positionOfCapturedPiece or whatIsMoving == color:
        gameState['halfmovesSinceLastCaptureOrPawnMove'] = 0
        gameState['positionsSinceLastCaptureOrPawnMove'] = defaultdict(int)
    else:
        if gameState['halfmovesSinceLastCaptureOrPawnMove'] == 99:
            gameState['status'] = 'Draw by 50-move-rule'
            return
        gameState['halfmovesSinceLastCaptureOrPawnMove'] += 1
    
    # Increment move number
    if color == -1:
        gameState['moveNumber'] += 1

    # Changing board state: special cases = [castling, pawn promotion, en passant], default = move the piece
    if whatIsMoving == king:
        gameState['kingPositions'][color] = finalPosition
        if move == ((castlingRowIndex, 4), (castlingRowIndex, 6), None):
            gameState['currentPosition']['pieces'][color].pop((castlingRowIndex, 7))
            gameState['currentPosition']['pieces'][color][(castlingRowIndex, 5)] = rook
            gameState['featureVector'][castlingRowIndex * 8 + 7] = 0
            gameState['featureVector'][castlingRowIndex * 8 + 5] = rook
        elif move == ((castlingRowIndex, 4), (castlingRowIndex, 2), None):
            gameState['currentPosition']['pieces'][color].pop((castlingRowIndex, 0))
            gameState['currentPosition']['pieces'][color][(castlingRowIndex, 3)] = rook
            gameState['featureVector'][castlingRowIndex * 8] = 0
            gameState['featureVector'][castlingRowIndex * 8 + 3] = rook
    if positionOfCapturedPiece:
        gameState['currentPosition']['pieces'][oppositeColor].pop(positionOfCapturedPiece)
        gameState['featureVector'][positionOfCapturedPiece[0] * 8 + positionOfCapturedPiece[1]] = 0
    gameState['currentPosition']['pieces'][color].pop(initialPosition)
    gameState['featureVector'][initialPosition[0] * 8 + initialPosition[1]] = 0
    if whatIsMoving == color and finalPosition[0] == promotionRowIndex:
        gameState['currentPosition']['pieces'][color][finalPosition] = queen
        gameState['featureVector'][finalPosition[0] * 8 + finalPosition[1]] = queen
    else:
        gameState['currentPosition']['pieces'][color][finalPosition] = whatIsMoving
        gameState['featureVector'][finalPosition[0] * 8 + finalPosition[1]] = whatIsMoving

    # Changing castling rights: if you move your king or one of your rooks for the first time, or if you capture one of your opponents rooks
    if initialPosition == (castlingRowIndex, 4):
        if gameState['currentPosition']['castlingRights'][color][0]:
            gameState['currentPosition']['castlingRights'][color][0] = 0
            gameState['featureVector'][kingsideCastlingRightFeatureVectorIndex] = 0
        if gameState['currentPosition']['castlingRights'][color][1]:
            gameState['currentPosition']['castlingRights'][color][1] = 0
            gameState['featureVector'][queensideCastlingRightFeatureVectorIndex] = 0
    elif initialPosition == (castlingRowIndex, 7) and gameState['currentPosition']['castlingRights'][color][0]:
        gameState['currentPosition']['castlingRights'][color][0] = 0
        gameState['featureVector'][kingsideCastlingRightFeatureVectorIndex] = 0
    elif initialPosition == (castlingRowIndex, 0) and gameState['currentPosition']['castlingRights'][color][1]:
        gameState['currentPosition']['castlingRights'][color][1] = 0
        gameState['featureVector'][queensideCastlingRightFeatureVectorIndex] = 0
    if finalPosition == (opponentCastlingRowIndex, 0) and gameState['currentPosition']['castlingRights'][oppositeColor][1]:
        gameState['currentPosition']['castlingRights'][oppositeColor][1] = 0
        gameState['featureVector'][queensideCastlingRightFeatureVectorIndex] = 0
    elif finalPosition == (opponentCastlingRowIndex, 7) and gameState['currentPosition']['castlingRights'][oppositeColor][0]:
        gameState['currentPosition']['castlingRights'][oppositeColor][0] = 0
        gameState['featureVector'][kingsideCastlingRightFeatureVectorIndex] = 0
    
    # Changing en passant square: If your move is a pawn double-jump, set the en passant square accordingly, else set it to None
    if whatIsMoving == color and initialPosition[0] == pawnDoubleJumpInitialRowIndex and finalPosition[0] == pawnDoubleJumpFinalRowIndex:
        gameState['currentPosition']['enPassantSquare'] = (newEnPassantSquareRowIndex, finalPosition[1])
        gameState['featureVector'][69], gameState['featureVector'][70] = newEnPassantSquareRowIndex, finalPosition[1]
    else:
        gameState['currentPosition']['enPassantSquare'] = None
        gameState['featureVector'][69], gameState['featureVector'][70] = -1, -1

    
    # Check for draw by threefold repetition:
    # "Two positions are by definition 'the same' if the same types of pieces occupy the same squares, the same player 
    # has the move, the remaining castling rights are the same and the possibility to capture en passant is the same."
    position = freeze(gameState['currentPosition'])
    if gameState['positionsSinceLastCaptureOrPawnMove'][position] == 2:
        gameState['status'] = 'Draw by threefold repetition'
        return
    else:
        gameState['positionsSinceLastCaptureOrPawnMove'][position] += 1

    # Check for draw by insufficient material:
    numWhitePieces = len(gameState['currentPosition']['pieces'][1])
    numBlackPieces = len(gameState['currentPosition']['pieces'][-1])
    numPieces = numWhitePieces + numBlackPieces
    if numWhitePieces == 2 and 4 in gameState['currentPosition']['pieces'][1].values() and numBlackPieces == 2 and -4 in gameState['currentPosition']['pieces'][-1].values():
        for pos, piece in gameState['currentPosition']['pieces'][1].items():
            if piece == 4:
                whiteBishopPos = pos
                break
        for pos, piece in gameState['currentPosition']['pieces'][-1].items():
            if piece == -4:
                blackBishopPos = pos
                break
        if (whiteBishopPos[0] + whiteBishopPos[1]) % 2 == (blackBishopPos[0] + blackBishopPos[1]) % 2:
            gameState['status'] = 'Draw by insufficient material (king and bishop versus king and bishop with the bishops on the same color)'
            return
    elif numPieces == 3:
        if numWhitePieces == 2:
            whitePieces = gameState['currentPosition']['pieces'][1].values()
            if 3 in whitePieces:
                gameState['status'] = 'Draw by insufficient material (king and knight versus king)'
                return
            if 4 in whitePieces:
                gameState['status'] = 'Draw by insufficient material (king and bishop versus king)'
                return
        else:
            blackPieces = gameState['currentPosition']['pieces'][-1].values()
            if -3 in blackPieces:
                gameState['status'] = 'Draw by insufficient material (king and knight versus king)'
                return
            if -4 in blackPieces:
                gameState['status'] = 'Draw by insufficient material (king and bishop versus king)'
                return
    elif numPieces == 2:
        gameState['status'] = 'Draw by insufficient material (king versus king)'
        return

    # Always change the active color to the opposite of what it currently is
    gameState['currentPosition']['activeColor'] *= -1
    gameState['featureVector'][64] *= -1

    gameState['Fen'] = gameStateToFen(gameState['currentPosition'], gameState['halfmovesSinceLastCaptureOrPawnMove'], gameState['moveNumber'])

    gameState['legalMoves'] = legalMoves(gameState['currentPosition'], gameState['kingPositions'][gameState['currentPosition']['activeColor']])

    if not len(gameState['legalMoves']):
        if isColorInCheck(gameState['currentPosition']['activeColor'], gameState['kingPositions'][gameState['currentPosition']['activeColor']], gameState['currentPosition']['pieces']):
            if color == 1:
                gameState['status'] = 'White checkmates black'
            else:
                gameState['status'] = 'Black checkmates white'
        else:
            if color == 1:
                gameState['status'] = 'White stalemates black'
            else:
                gameState['status'] = 'Black stalemates white'
        return



####################
# Debugging section
####################

symbols = {
    0: ' ', -1: '♟', -2: '♜', -3: '♞', -4: '♝', -5: '♛', -6: '♚', 
    1: '♙', 2: '♖', 3: '♘', 4: '♗', 5: '♕', 6: '♔'
}

def displayBoard(pieces):
    boardMatrix = [[0] * 8 for i in range(8)]
    for x in pieces.values():
        for pos, piece in x.items():
            boardMatrix[pos[0]][pos[1]] = piece
    print(' --- --- --- --- --- --- --- --- ')
    for i in range(8):
        print('| ' + ' '.join(map(lambda x : symbols[x] + ' |', boardMatrix[i])))
        print(' --- --- --- --- --- --- --- --- ')
    print()


def runGames(numGames):
    results = defaultdict(int)
    for i in tqdm(range(numGames)):
        gameState = getFreshGameState_trackingFeatureVector()
        numHalfmoves = 0
        while gameState['status'] == 'live' and numHalfmoves != 80:
            executeMove_trackingFeatureVector(random.choice(tuple(gameState['legalMoves'])), gameState)
            numHalfmoves += 1
            # print(gameState['Fen'])
            # displayBoard(gameState['currentPosition']['pieces'])
        # print(gameState['status'])
    for key, value in results.items():
        print(f'{key}: {value}')


# runGames(1000)
