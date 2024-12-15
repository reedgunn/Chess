##########################
# Initializing game state:
##########################

pieceOrder = ('rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook')
def getFreshPieces():
    res = {}
    for x in {('black', 0, 1), ('white', 7, 6)}:
        res[x[0]] = {}
        for i in range(8):
            res[x[0]][(x[1], i)] = pieceOrder[i]
            res[x[0]][(x[2], i)] = 'pawn'
    return res

encodedPieceOrder = (2, 3, 4, 5, 6, 4, 3, 2)
def getFreshFeatureVector():
    res = [0] * 71
    for x in {(-1, 0, 1), (1, 7, 6)}:
        for i in range(8):
            res[x[1] * 8 + i] = encodedPieceOrder[i] * x[0]
            res[x[2] * 8 + i] = x[0]
    for i in range(64, 69):
        res[i] = 1
    for i in range(69, 71):
        res[i] = -1
    return res

def getFreshGameState():
    res = {}
    res['vitals'] = {
        'pieces': getFreshPieces(),
        'whoseTurnIsIt': 'white',
        'castlingRights': {color : {f'{side}side' : True for side in {'king', 'queen'}} for color in {'black', 'white'}},
        'enPassantSquare': None
    }
    res['kingPositions'] = {x[0] : (x[1], 4) for x in {('black', 0), ('white', 7)}}
    res['featureVector'] = getFreshFeatureVector()
    res['vitalssSinceLastCaptureOrPawnMove'] = {tuple(res['featureVector']): 1}
    res['halfmovesSinceLastCaptureOrPawnMove'] = 0
    res['legalMoves'] = legalMoves(res['vitals'], 'black', res['kingPositions'][res['vitals']['whoseTurnIsIt']])
    res['status'] = 'live'
    res['moveNumber'] = 1
    res['Fen'] = gameStateToFen(res['vitals'], res['halfmovesSinceLastCaptureOrPawnMove'], res['moveNumber'])
    return res


#############################################
# Conversion from game state to FEN notation:
#############################################

blackEncodedPieceToFenPiece = {'pawn': 'p', 'rook': 'r', 'knight': 'n', 'bishop': 'b', 'queen': 'q', 'king': 'k'}
whiteEncodedPieceToFenPiece = {'pawn': 'P', 'rook': 'R', 'knight': 'N', 'bishop': 'B', 'queen': 'Q', 'king': 'K'}
fenRows = ('8', '7', '6', '5', '4', '3', '2', '1')
fenColumns = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
def gameStateToFen(vitals, halfmovesSinceLastCaptureOrPawnMove, moveNumber):
    res = ''
    for i in range(8):
        emptySquaresCount = 0
        for j in range(8):
            position = (i, j)
            if position not in vitals['pieces']['black'] and position not in vitals['pieces']['white']:
                emptySquaresCount += 1
            else:
                if emptySquaresCount:
                    res += str(emptySquaresCount)
                    emptySquaresCount = 0
                if position in vitals['pieces']['black']:
                    res += blackEncodedPieceToFenPiece[vitals['pieces']['black'][position]]
                else:
                    res += whiteEncodedPieceToFenPiece[vitals['pieces']['white'][position]]
        if emptySquaresCount:
            res += str(emptySquaresCount)
        if i != 7:
            res += '/'
    res += f' {vitals['whoseTurnIsIt'][0]} '
    castlingRights = ''
    for x in (('white', 'K', 'Q'), ('black', 'k', 'q')):
        for y in (('king', 1), ('queen', 2)):
            if vitals['castlingRights'][x[0]][f'{y[0]}side']:
                castlingRights += x[y[1]]
    res += castlingRights if castlingRights else '-'
    res += f' {fenColumns[vitals['enPassantSquare'][1]]}{fenRows[vitals['enPassantSquare'][0]]} ' if vitals['enPassantSquare'] else ' - '
    res += f'{halfmovesSinceLastCaptureOrPawnMove} {moveNumber}'
    return res


##########################################
# Calculating squares threatened by color:
##########################################

def isEmpty(position, pieces):
    return position not in pieces['black'] and position not in pieces['white']

def getForwardRowIndexChange(color):
    return 1 if color == 'black' else -1

def squaresThreatenedByPawn(position, color):
    res = set()
    forwardRowIndexChange = getForwardRowIndexChange(color)
    finalRowIndex = position[0] + forwardRowIndexChange
    for x in {(0, -1), (7, 1)}:
        if position[1] != x[0]:
            res.add((finalRowIndex, position[1] + x[1]))
    return res

def squaresThreatenedByRook(position, pieces):
    res = set()
    for posIndexPointer in {0, 1}:
        for positionChange, bound in {(-1, -1), (1, 8)}:
            curPos = list(position)
            curPos[posIndexPointer] += positionChange
            while curPos[posIndexPointer] != bound:
                addition = tuple(curPos)
                res.add(addition)
                if not isEmpty(addition, pieces):
                    break
                curPos[posIndexPointer] += positionChange
    return res

def squaresThreatenedByKnight(position):
    res = set()
    notOnTopEdge = position[0] != 0
    notOnRightEdge = position[1] != 7
    notOnBottomEdge = position[0] != 7
    notOnLeftEdge = position[1] != 0
    upByOneRowIndex = position[0] - 1
    downByOneRowIndex = position[0] + 1
    rightByOneColumnIndex = position[1] + 1
    leftByOneColumnIndex = position[1] - 1
    # Big up
    if notOnTopEdge and position[0] != 1: # not close to top edge
        upByTwoRowIndex = position[0] - 2
        # Small left
        if notOnLeftEdge:
            res.add((upByTwoRowIndex, leftByOneColumnIndex))
        # Small right
        if notOnRightEdge:
            res.add((upByTwoRowIndex, rightByOneColumnIndex))
    # Big right
    if notOnRightEdge and position[1] != 6: # not close to right edge
        rightByTwoColumnIndex = position[1] + 2
        # Small up
        if notOnTopEdge:
            res.add((upByOneRowIndex, rightByTwoColumnIndex))
        # Small down
        if notOnBottomEdge:
            res.add((downByOneRowIndex, rightByTwoColumnIndex))
    # Big down
    if notOnBottomEdge and position[0] != 6: # not close to bottom edge
        downByTwoRowIndex = position[0] + 2
        # Small right
        if notOnRightEdge:
            res.add((downByTwoRowIndex, rightByOneColumnIndex))
        # Small left
        if notOnLeftEdge:
            res.add((downByTwoRowIndex, leftByOneColumnIndex))
    # Big left
    if notOnLeftEdge and position[1] != 1: # not close to left edge
        leftByTwoColumnIndex = position[1] - 2
        # Small down
        if notOnBottomEdge:
            res.add((downByOneRowIndex, leftByTwoColumnIndex))
        # Small up
        if notOnTopEdge:
            res.add((upByOneRowIndex, leftByTwoColumnIndex))
    return res

def squaresThreatenedByBishop(position, pieces):
    res = set()
    for rowIndexChange, rowIndexBound in {(-1, -1), (1, 8)}:
        for columnIndexChange, columnIndexBound in {(-1, -1), (1, 8)}:
            curPos = [position[0] + rowIndexChange, position[1] + columnIndexChange]
            while curPos[0] != rowIndexBound and curPos[1] != columnIndexBound:
                addition = tuple(curPos)
                res.add(addition)
                if not isEmpty(addition, pieces):
                    break
                curPos[0] += rowIndexChange
                curPos[1] += columnIndexChange
    return res

def squaresThreatenedByQueen(position, pieces):
    return squaresThreatenedByRook(position, pieces) | squaresThreatenedByBishop(position, pieces)

def squaresThreatenedByKing(position):
    res = set()
    notOnRightEdge = position[1] != 7
    notOnLeftEdge = position[1] != 0
    rightByOneColumnIndex = position[1] + 1
    leftByOneColumnIndex = position[1] - 1
    # North:
    if position[0] != 0: # not on top edge
        upByOneRowIndex = position[0] - 1
        # North:
        res.add((upByOneRowIndex, position[1]))
        # Northwest:
        if notOnLeftEdge:
            res.add((upByOneRowIndex, leftByOneColumnIndex))
        # Northeast:
        if notOnRightEdge:
            res.add((upByOneRowIndex, rightByOneColumnIndex))
    # South:
    if position[0] != 7: # not on bottom edge
        downByOneRowIndex = position[0] + 1
        # South:
        res.add((downByOneRowIndex, position[1]))
        # Southwest:
        if notOnLeftEdge:
            res.add((downByOneRowIndex, leftByOneColumnIndex))
        # Southeast:
        if notOnRightEdge:
            res.add((downByOneRowIndex, rightByOneColumnIndex))
    # West:
    if notOnLeftEdge:
        res.add((position[0], leftByOneColumnIndex))
    # East:
    if notOnRightEdge:
        res.add((position[0], rightByOneColumnIndex))
    return res

def squaresThreatenedByColor(pieces, color):
    res = set()
    for position, piece in pieces[color].items():
        if piece == 'pawn':
            res.update(squaresThreatenedByPawn(position, color))
        elif piece == 'rook':
            res.update(squaresThreatenedByRook(position, pieces))
        elif piece == 'knight':
            res.update(squaresThreatenedByKnight(position))
        elif piece == 'bishop':
            res.update(squaresThreatenedByBishop(position, pieces))
        elif piece == 'queen':
            res.update(squaresThreatenedByQueen(position, pieces))
        else:
            res.update(squaresThreatenedByKing(position))
    return res


##########################
# Calculating legal moves:
##########################

def getOppositeColor(color):
    return 'white' if color == 'black' else 'black'

def isColorInCheck(oppositeColor, kingPosition, pieces):
    return kingPosition in squaresThreatenedByColor(pieces, oppositeColor)

# move: (initial position, final position, position of captured piece [or None if the move isn't a capture])

def doesMoveLeaveKingInCheck(move, color, oppositeColor, kingPosition, pieces):
    pieces[color][move[1]] = pieces[color].pop(move[0])
    capturedPiece = pieces[oppositeColor].pop(move[2]) if move[2] else None
    res = isColorInCheck(oppositeColor, kingPosition, pieces)
    if capturedPiece:
        pieces[oppositeColor][move[2]] = capturedPiece
    pieces[color][move[0]] = pieces[color].pop(move[1])
    return res
    
def addMoveToResIfDoesntLeaveKingInCheck(res, move, color, oppositeColor, kingPosition, pieces):
    if not doesMoveLeaveKingInCheck(move, color, oppositeColor, kingPosition, pieces):
        res.add(move)

def pawnLegalMoves(position, color, oppositeColor, kingPosition, pieces, enPassantSquare):
    res = set()
    doubleJumpStartingRowIndex = 1 if color == 'black' else 6
    forwardRowIndexChange = getForwardRowIndexChange(color)
    singleHopFinalPosition = (position[0] + forwardRowIndexChange, position[1])
    if isEmpty(singleHopFinalPosition, pieces):
        addMoveToResIfDoesntLeaveKingInCheck(res, (position, singleHopFinalPosition, None), color, oppositeColor, kingPosition, pieces)
        if position[0] == doubleJumpStartingRowIndex:
            doubleHopFinalPosition = (position[0] + 2 * forwardRowIndexChange, position[1])
            if isEmpty(doubleHopFinalPosition, pieces):
                addMoveToResIfDoesntLeaveKingInCheck(res, (position, doubleHopFinalPosition, None), color, oppositeColor, kingPosition, pieces)
    for columnIndexChange, columnIndexBound in {(-1, 0), (1, 7)}:
        if position[1] != columnIndexBound:
            captureFinalPosition = (singleHopFinalPosition[0], position[1] + columnIndexChange)
            if captureFinalPosition in pieces[oppositeColor]:
                addMoveToResIfDoesntLeaveKingInCheck(res, (position, captureFinalPosition, captureFinalPosition), color, oppositeColor, kingPosition, pieces)
            elif captureFinalPosition == enPassantSquare:
                addMoveToResIfDoesntLeaveKingInCheck(res, (position, captureFinalPosition, (position[0], captureFinalPosition[1])), color, oppositeColor, kingPosition, pieces)
    return res

def rookLegalMoves(position, color, oppositeColor, pieces, kingPosition):
    res = set()
    for posIndexPointer in {0, 1}:
        for positionChange, bound in {(-1, -1), (1, 8)}:
            curPos = list(position)
            curPos[posIndexPointer] += positionChange
            while curPos[posIndexPointer] != bound:
                possibleAddition = tuple(curPos)
                if possibleAddition in pieces[color]:
                    break
                if possibleAddition in pieces[oppositeColor]:
                    addMoveToResIfDoesntLeaveKingInCheck(res, (position, possibleAddition, possibleAddition), color, oppositeColor, kingPosition, pieces)
                    break
                else:
                    addMoveToResIfDoesntLeaveKingInCheck(res, (position, possibleAddition, None), color, oppositeColor, kingPosition, pieces)
                curPos[posIndexPointer] += positionChange
    return res

def hoppingPieceLegalMoveHelper(res, possibleMoveFinalPosition, possibleMoveInitialPosition, color, oppositeColor, kingPosition, pieces):
    if possibleMoveFinalPosition not in pieces[color]:
        if possibleMoveFinalPosition in pieces[oppositeColor]:
            addMoveToResIfDoesntLeaveKingInCheck(res, (possibleMoveInitialPosition, possibleMoveFinalPosition, possibleMoveFinalPosition), color, oppositeColor, kingPosition, pieces)
        else:
            addMoveToResIfDoesntLeaveKingInCheck(res, (possibleMoveInitialPosition, possibleMoveFinalPosition, None), color, oppositeColor, kingPosition, pieces)

def knightLegalMoves(position, color, oppositeColor, kingPosition, pieces):
    res = set()
    notOnTopEdge = position[0] != 0
    notOnRightEdge = position[1] != 7
    notOnBottomEdge = position[0] != 7
    notOnLeftEdge = position[1] != 0
    upByOneRowIndex = position[0] - 1
    downByOneRowIndex = position[0] + 1
    rightByOneColumnIndex = position[1] + 1
    leftByOneColumnIndex = position[1] - 1
    # Big up
    if notOnTopEdge and position[0] != 1: # not close to top edge
        upByTwoRowIndex = position[0] - 2
        # Small left
        if notOnLeftEdge:
            hoppingPieceLegalMoveHelper(res, (upByTwoRowIndex, leftByOneColumnIndex), position, color, oppositeColor, kingPosition, pieces)
        # Small right
        if notOnRightEdge:
            hoppingPieceLegalMoveHelper(res, (upByTwoRowIndex, rightByOneColumnIndex), position, color, oppositeColor, kingPosition, pieces)
    # Big right
    if notOnRightEdge and position[1] != 6: # not close to right edge
        rightByTwoColumnIndex = position[1] + 2
        # Small up
        if notOnTopEdge:
            hoppingPieceLegalMoveHelper(res, (upByOneRowIndex, rightByTwoColumnIndex), position, color, oppositeColor, kingPosition, pieces)
        # Small down
        if notOnBottomEdge:
            hoppingPieceLegalMoveHelper(res, (downByOneRowIndex, rightByTwoColumnIndex), position, color, oppositeColor, kingPosition, pieces)
    # Big down
    if notOnBottomEdge and position[0] != 6: # not close to bottom edge
        downByTwoRowIndex = position[0] + 2
        # Small right
        if notOnRightEdge:
            hoppingPieceLegalMoveHelper(res, (downByTwoRowIndex, rightByOneColumnIndex), position, color, oppositeColor, kingPosition, pieces)
        # Small left
        if notOnLeftEdge:
            hoppingPieceLegalMoveHelper(res, (downByTwoRowIndex, leftByOneColumnIndex), position, color, oppositeColor, kingPosition, pieces)
    # Big left
    if notOnLeftEdge and position[1] != 1: # not close to left edge
        leftByTwoColumnIndex = position[1] - 2
        # Small down
        if notOnBottomEdge:
            hoppingPieceLegalMoveHelper(res, (downByOneRowIndex, leftByTwoColumnIndex), position, color, oppositeColor, kingPosition, pieces)
        # Small up
        if notOnTopEdge:
            hoppingPieceLegalMoveHelper(res, (upByOneRowIndex, leftByTwoColumnIndex), position, color, oppositeColor, kingPosition, pieces)
    return res

def bishopLegalMoves(position, color, oppositeColor, pieces, kingPosition):
    res = set()
    for rowIndexChange, rowIndexBound in {(-1, -1), (1, 8)}:
        for columnIndexChange, columnIndexBound in {(-1, -1), (1, 8)}:
            curPos = [position[0] + rowIndexChange, position[1] + columnIndexChange]
            while curPos[0] != rowIndexBound and curPos[1] != columnIndexBound:
                possibleAddition = tuple(curPos)
                if possibleAddition in pieces[color]:
                    break
                if possibleAddition in pieces[oppositeColor]:
                    addMoveToResIfDoesntLeaveKingInCheck(res, (position, possibleAddition, possibleAddition), color, oppositeColor, kingPosition, pieces)
                    break
                else:
                    addMoveToResIfDoesntLeaveKingInCheck(res, (position, possibleAddition, None), color, oppositeColor, kingPosition, pieces)
                curPos[0] += rowIndexChange
                curPos[1] += columnIndexChange
    return res

def queenLegalMoves(position, color, oppositeColor, pieces, kingPosition):
    return rookLegalMoves(position, color, oppositeColor, pieces, kingPosition) | bishopLegalMoves(position, color, oppositeColor, pieces, kingPosition)

def kingLegalMoves(position, color, oppositeColor, pieces, castlingRights):
    res = set()
    notOnRightEdge = position[1] != 7
    notOnLeftEdge = position[1] != 0
    rightByOneColumnIndex = position[1] + 1
    leftByOneColumnIndex = position[1] - 1
    # North:
    if position[0] != 0: # not on top edge
        upByOneRowIndex = position[0] - 1
        # North:
        possibleMoveFinalPosition = (upByOneRowIndex, position[1])
        hoppingPieceLegalMoveHelper(res, possibleMoveFinalPosition, position, color, oppositeColor, possibleMoveFinalPosition, pieces)
        # Northwest:
        if notOnLeftEdge:
            possibleMoveFinalPosition = (upByOneRowIndex, leftByOneColumnIndex)
            hoppingPieceLegalMoveHelper(res, possibleMoveFinalPosition, position, color, oppositeColor, possibleMoveFinalPosition, pieces)
        # Northeast:
        if notOnRightEdge:
            possibleMoveFinalPosition = (upByOneRowIndex, rightByOneColumnIndex)
            hoppingPieceLegalMoveHelper(res, possibleMoveFinalPosition, position, color, oppositeColor, possibleMoveFinalPosition, pieces)
    # South:
    if position[0] != 7: # not on bottom edge
        downByOneRowIndex = position[0] + 1
        # South:
        possibleMoveFinalPosition = (downByOneRowIndex, position[1])
        hoppingPieceLegalMoveHelper(res, possibleMoveFinalPosition, position, color, oppositeColor, possibleMoveFinalPosition, pieces)
        # Southwest:
        if notOnLeftEdge:
            possibleMoveFinalPosition = (downByOneRowIndex, leftByOneColumnIndex)
            hoppingPieceLegalMoveHelper(res, possibleMoveFinalPosition, position, color, oppositeColor, possibleMoveFinalPosition, pieces)
        # Southeast:
        if notOnRightEdge:
            possibleMoveFinalPosition = (downByOneRowIndex, rightByOneColumnIndex)
            hoppingPieceLegalMoveHelper(res, possibleMoveFinalPosition, position, color, oppositeColor, possibleMoveFinalPosition, pieces)
    # West:
    if notOnLeftEdge:
        possibleMoveFinalPosition = (position[0], leftByOneColumnIndex)
        hoppingPieceLegalMoveHelper(res, possibleMoveFinalPosition, position, color, oppositeColor, possibleMoveFinalPosition, pieces)
    # East:
    if notOnRightEdge:
        possibleMoveFinalPosition = (position[0], rightByOneColumnIndex)
        hoppingPieceLegalMoveHelper(res, possibleMoveFinalPosition, position, color, oppositeColor, possibleMoveFinalPosition, pieces)
    # Castling:
    squaresThreatenedByOpponent = squaresThreatenedByColor(pieces, oppositeColor)
    if position not in squaresThreatenedByOpponent: # if we aren't currently in check, then we might be able to castle
        castlingRowIndex = 0 if color == 'black' else 7
        if castlingRights['kingside']:
            squareOneToRightOfKing = (castlingRowIndex, 5)
            if isEmpty(squareOneToRightOfKing, pieces) and squareOneToRightOfKing not in squaresThreatenedByOpponent:
                squareTwoToRightOfKing = (castlingRowIndex, 6)
                if isEmpty(squareTwoToRightOfKing, pieces) and squareTwoToRightOfKing not in squaresThreatenedByOpponent:
                    res.add((position, squareTwoToRightOfKing, None))
        if castlingRights['queenside']:
            squareOneToLeftOfKing = (castlingRowIndex, 3)
            if isEmpty(squareOneToLeftOfKing, pieces) and squareOneToLeftOfKing not in squaresThreatenedByOpponent:
                squareTwoToLeftOfKing = (castlingRowIndex, 2)
                if isEmpty(squareTwoToLeftOfKing, pieces) and squareTwoToLeftOfKing not in squaresThreatenedByOpponent and isEmpty((castlingRowIndex, 1), pieces):
                    res.add((position, squareTwoToLeftOfKing, None))
    return res

def legalMoves(vitals, oppositeColor, kingPosition):
    res = set()
    for position, piece in vitals['pieces'][vitals['whoseTurnIsIt']].copy().items():
        if piece == 'pawn':
            res.update(pawnLegalMoves(position, vitals['whoseTurnIsIt'], oppositeColor, kingPosition, vitals['pieces'], vitals['enPassantSquare']))
        elif piece == 'rook':
            res.update(rookLegalMoves(position, vitals['whoseTurnIsIt'], oppositeColor, vitals['pieces'], kingPosition))
        elif piece == 'knight':
            res.update(knightLegalMoves(position, vitals['whoseTurnIsIt'], oppositeColor, kingPosition, vitals['pieces']))
        elif piece == 'bishop':
            res.update(bishopLegalMoves(position, vitals['whoseTurnIsIt'], oppositeColor, vitals['pieces'], kingPosition))
        elif piece == 'queen':
            res.update(queenLegalMoves(position, vitals['whoseTurnIsIt'], oppositeColor, vitals['pieces'], kingPosition))
        else:
            res.update(kingLegalMoves(position, vitals['whoseTurnIsIt'], oppositeColor, vitals['pieces'], vitals['castlingRights'][vitals['whoseTurnIsIt']]))
    return res


####################################
# Executing moves on the game state:
####################################

def executeMove(move, gameState):
    if gameState['vitals']['whoseTurnIsIt'] == 'black':
        color = 'black'
        oppositeColor = 'white'
        pieceTypeToEncodedPiece = {
            'pawn': -1,
            'rook': -2,
            'knight': -3,
            'bishop': -4,
            'queen': -5,
            'king': -6
        }
        promotionRowIndex = 7
        castlingRowIndex = 0
        opponentCastlingRowIndex = 7
        pawnDoubleJumpInitialRowIndex = 1
        pawnDoubleJumpFinalRowIndex = 3
        newEnPassantSquareRowIndex = 2
        kingsideCastlingRightFeatureVectorIndex = 67
        queensideCastlingRightFeatureVectorIndex = 68
        opponentKingsideCastlingRightFeatureVectorIndex = 65
        opponentQueensideCastlingRightFeatureVectorIndex = 66
    else:
        color = 'white'
        oppositeColor = 'black'
        pieceTypeToEncodedPiece = {
            'pawn': 1,
            'rook': 2,
            'knight': 3,
            'bishop': 4,
            'queen': 5,
            'king': 6
        }
        promotionRowIndex = 0
        castlingRowIndex = 7
        opponentCastlingRowIndex = 0
        pawnDoubleJumpInitialRowIndex = 6
        pawnDoubleJumpFinalRowIndex = 4
        newEnPassantSquareRowIndex = 5
        kingsideCastlingRightFeatureVectorIndex = 65
        queensideCastlingRightFeatureVectorIndex = 66
        opponentKingsideCastlingRightFeatureVectorIndex = 67
        opponentQueensideCastlingRightFeatureVectorIndex = 68
        
    whatIsMoving = gameState['vitals']['pieces'][color].pop(move[0])
    gameState['featureVector'][move[0][0] * 8 + move[0][1]] = 0

    # Changing halfmovesSinceLastCaptureOrPawnMove: If the move is a capture or a pawn move, set to 0, otherwise increment by 1
    if move[2] or whatIsMoving == 'pawn':
        gameState['halfmovesSinceLastCaptureOrPawnMove'] = 0
        gameState['vitalssSinceLastCaptureOrPawnMove'] = {}
    else:
        if gameState['halfmovesSinceLastCaptureOrPawnMove'] == 99:
            gameState['status'] = 'Draw by 50-move-rule'
            return
        gameState['halfmovesSinceLastCaptureOrPawnMove'] += 1
    
    # Increment move number
    if color == 'black':
        gameState['moveNumber'] += 1

    # Changing board state: special cases = [castling, pawn promotion, en passant], default = move the piece
    # For castling, have to move the rook (the king is already moved later):
    if whatIsMoving == 'king':
        gameState['kingPositions'][color] = move[1]
        for side in gameState['vitals']['castlingRights'][color]:
            gameState['vitals']['castlingRights'][color][side] = False
        for i in {kingsideCastlingRightFeatureVectorIndex, queensideCastlingRightFeatureVectorIndex}:
            gameState['featureVector'][i] = 0
        if move == ((castlingRowIndex, 4), (castlingRowIndex, 6), None):
            gameState['vitals']['pieces'][color].pop((castlingRowIndex, 7))
            gameState['featureVector'][castlingRowIndex * 8 + 7] = 0
            gameState['vitals']['pieces'][color][(castlingRowIndex, 5)] = 'rook'
            gameState['featureVector'][castlingRowIndex * 8 + 5] = pieceTypeToEncodedPiece['rook']
        elif move == ((castlingRowIndex, 4), (castlingRowIndex, 2), None):
            gameState['vitals']['pieces'][color].pop((castlingRowIndex, 0))
            gameState['featureVector'][castlingRowIndex * 8] = 0
            gameState['vitals']['pieces'][color][(castlingRowIndex, 3)] = 'rook'
            gameState['featureVector'][castlingRowIndex * 8 + 3] = pieceTypeToEncodedPiece['rook']
    # Handling captures:
    if move[2]:
        gameState['vitals']['pieces'][oppositeColor].pop(move[2])
        gameState['featureVector'][move[2][0] * 8 + move[2][1]] = 0
    
    if whatIsMoving == 'pawn' and move[1][0] == promotionRowIndex:
        gameState['vitals']['pieces'][color][move[1]] = 'queen'
        gameState['featureVector'][move[1][0] * 8 + move[1][1]] = pieceTypeToEncodedPiece['queen']
    else:
        gameState['vitals']['pieces'][color][move[1]] = whatIsMoving
        gameState['featureVector'][move[1][0] * 8 + move[1][1]] = pieceTypeToEncodedPiece[whatIsMoving]

    # Changing castling rights (we already handled the case where we move our king)
    # If you one of your rooks for the first time, need to modify your castling rights
    if move[0] == (castlingRowIndex, 7):
        gameState['vitals']['castlingRights'][color]['kingside'] = 0
        gameState['featureVector'][kingsideCastlingRightFeatureVectorIndex] = 0
    elif move[0] == (castlingRowIndex, 0):
        gameState['vitals']['castlingRights'][color]['queenside'] = 0
        gameState['featureVector'][queensideCastlingRightFeatureVectorIndex] = 0
    # If you capture one of your opponents rooks, possibly need to modify their castling rights
    if move[1] == (opponentCastlingRowIndex, 0):
        gameState['vitals']['castlingRights'][oppositeColor]['queenside'] = 0
        gameState['featureVector'][opponentQueensideCastlingRightFeatureVectorIndex] = 0
    elif move[1] == (opponentCastlingRowIndex, 7):
        gameState['vitals']['castlingRights'][oppositeColor]['kingside'] = 0
        gameState['featureVector'][opponentKingsideCastlingRightFeatureVectorIndex] = 0
    
    # Changing en passant square: If your move is a pawn double-jump, set the en passant square accordingly, otherwise set it to None
    if whatIsMoving == 'pawn' and move[0][0] == pawnDoubleJumpInitialRowIndex and move[1][0] == pawnDoubleJumpFinalRowIndex:
        gameState['vitals']['enPassantSquare'] = (newEnPassantSquareRowIndex, move[1][1])
        gameState['featureVector'][69], gameState['featureVector'][70] = newEnPassantSquareRowIndex, move[1][1]
    else:
        gameState['vitals']['enPassantSquare'] = None
        gameState['featureVector'][69], gameState['featureVector'][70] = -1, -1
    
    # Check for draw by threefold repetition:
    # "Two positions are by definition 'the same' if the same types of pieces occupy the same squares, the same player 
    # has the move, the remaining castling rights are the same and the possibility to capture en passant is the same."
    vitals = tuple(gameState['featureVector'])
    if vitals in gameState['vitalssSinceLastCaptureOrPawnMove']:
        if gameState['vitalssSinceLastCaptureOrPawnMove'][vitals] == 2:
            gameState['status'] = 'Draw by threefold repetition'
            return
        gameState['vitalssSinceLastCaptureOrPawnMove'][vitals] += 1
    else:
        gameState['vitalssSinceLastCaptureOrPawnMove'][vitals] = 1

    # Check for draw by insufficient material:
    blackPieces = gameState['vitals']['pieces']['black'].values()
    whitePieces = gameState['vitals']['pieces']['white'].values()
    numPieces = len(blackPieces) + len(whitePieces)
    if numPieces == 4 and len(blackPieces) == 2 and len(whitePieces) == 2 and 'bishop' in blackPieces and 'bishop' in whitePieces:
        for position, piece in gameState['vitals']['pieces']['white'].items():
            if piece == 'bishop':
                whiteBishopPos = position
                break
        for position, piece in gameState['vitals']['pieces']['black'].items():
            if piece == 'bishop':
                blackBishopPos = position
                break
        if (whiteBishopPos[0] + whiteBishopPos[1]) % 2 == (blackBishopPos[0] + blackBishopPos[1]) % 2:
            gameState['status'] = 'Draw by insufficient material (king and bishop versus king and bishop with the bishops on the same color)'
            return
    elif numPieces == 3:
        if 'knight' in blackPieces or 'bishop' in blackPieces or 'knight' in whitePieces or 'bishop' in whitePieces:
            gameState['status'] = 'Draw by insufficient material (king and knight/bishop versus king)'
            return
    elif numPieces == 2:
        gameState['status'] = 'Draw by insufficient material (king versus king)'
        return

    # Always change the active color to the opposite of what it currently is
    gameState['vitals']['whoseTurnIsIt'] = oppositeColor
    gameState['featureVector'][64] *= -1

    gameState['Fen'] = gameStateToFen(gameState['vitals'], gameState['halfmovesSinceLastCaptureOrPawnMove'], gameState['moveNumber'])

    gameState['legalMoves'] = legalMoves(gameState['vitals'], color, gameState['kingPositions'][oppositeColor])

    if not len(gameState['legalMoves']):
        if isColorInCheck(color, gameState['kingPositions'][oppositeColor], gameState['vitals']['pieces']):
            gameState['status'] = f'{color} checkmates {oppositeColor}'
        else:
            gameState['status'] = f'{color} stalemates {oppositeColor}'
        return


####################
# Testing/debugging:
####################

from collections import defaultdict
import random
from tqdm import tqdm
import time

symbols = {
    0: ' ', -1: '♟', -2: '♜', -3: '♞', -4: '♝', -5: '♛', -6: '♚', 
    1: '♙', 2: '♖', 3: '♘', 4: '♗', 5: '♕', 6: '♔'
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
        gameState = getFreshGameState()
        while True:
            # print(gameState['Fen'])
            # displayBoard(gameState['featureVector'])
            # time.sleep(1.5)
            executeMove(random.choice(tuple(gameState['legalMoves'])), gameState)
            if gameState['status'] != 'live':
                displayBoard(gameState['featureVector'])
                print(gameState['status'])
                results[gameState['status']] += 1
                break
    for key, value in results.items():
        print(f'{key}: {value}')

# runGames(300)
