from copy import deepcopy


###################
# Constants:
###################

(
    ROOK,
    KNIGHT,
    BISHOP,
    QUEEN,
    KING,
    PAWN
) = range(6)

(
    BLACK_ROOK,
    BLACK_KNIGHT,
    BLACK_BISHOP,
    BLACK_QUEEN,
    BLACK_KING,
    BLACK_PAWN,
    EMPTY_SQUARE,
    WHITE_PAWN,
    WHITE_ROOK,
    WHITE_KNIGHT,
    WHITE_BISHOP,
    WHITE_QUEEN,
    WHITE_KING
) = range(13)


NA = -1

(
    WHITE,
    BLACK
) = range(2)

(
    PRESENT,
    ABSENT
) = range(2)

(
    ROW_8,
    ROW_7,
    ROW_6,
    ROW_5,
    ROW_4,
    ROW_3,
    ROW_2,
    ROW_1
) = range(8)

(
    COLUMN_A,
    COLUMN_B,
    COLUMN_C,
    COLUMN_D,
    COLUMN_E,
    COLUMN_F,
    COLUMN_G,
    COLUMN_H
) = range(8)

(
    LIVE,
    DRAW_BY_50_MOVE_RULE,
    DRAW_BY_THREEFOLD_REPETITION,
    DRAW_BY_INSUFFICIENT_MATERIAL,
    CHECKMATE,
    STALEMATE
) = range(6)

encodedStatusToStatus = ('live', 'draw by 50-move rule', 'draw by threefold repetition', 'draw by insufficient material', 'checkmate', 'stalemate')

(
    KINGSIDE_CASTLING_RIGHT_INDEX,
    QUEENSIDE_CASTLING_RIGHT_INDEX
) = range(2)

# 'freshGameState' is to be deepcopied for every new game
freshGameState = {
    # 'vitals' contains only all of the information that is relevant when deciding what move to make
    'vitals': {
        'pieces': {
            BLACK: {
                (ROW_8, COLUMN_A): ROOK, (ROW_8, COLUMN_B): KNIGHT, (ROW_8, COLUMN_C): BISHOP, (ROW_8, COLUMN_D): QUEEN, (ROW_8, COLUMN_E): KING, (ROW_8, COLUMN_F): BISHOP, (ROW_8, COLUMN_G): KNIGHT, (ROW_8, COLUMN_H): ROOK,
                (ROW_7, COLUMN_A): PAWN, (ROW_7, COLUMN_B): PAWN,   (ROW_7, COLUMN_C): PAWN,   (ROW_7, COLUMN_D): PAWN,  (ROW_7, COLUMN_E): PAWN, (ROW_7, COLUMN_F): PAWN,   (ROW_7, COLUMN_G): PAWN,   (ROW_7, COLUMN_H): PAWN
            },
            WHITE: {
                (ROW_2, COLUMN_A): PAWN, (ROW_2, COLUMN_B): PAWN,   (ROW_2, COLUMN_C): PAWN,   (ROW_2, COLUMN_D): PAWN,  (ROW_2, COLUMN_E): PAWN, (ROW_2, COLUMN_F): PAWN,   (ROW_2, COLUMN_G): PAWN,   (ROW_2, COLUMN_H): PAWN,
                (ROW_1, COLUMN_A): ROOK, (ROW_1, COLUMN_B): KNIGHT, (ROW_1, COLUMN_C): BISHOP, (ROW_1, COLUMN_D): QUEEN, (ROW_1, COLUMN_E): KING, (ROW_1, COLUMN_F): BISHOP, (ROW_1, COLUMN_G): KNIGHT, (ROW_1, COLUMN_H): ROOK
            }
        },
        'whoseTurnItIs': WHITE,
        'castlingRights': {
            WHITE: [
                # White kingside castling right:
                PRESENT,
                # White queenside castling right:
                PRESENT
            ],
            BLACK: [
                # Black kingside castling right:
                PRESENT,
                # Black queenside castling right:
                PRESENT
            ]
        },
        'enPassantSquare': None
    },
    'kingPositions': { BLACK: (ROW_8, COLUMN_E), WHITE: (ROW_1, COLUMN_E) },
    'featureVector': [
        # Board squares (0-63):
        BLACK_ROOK,   BLACK_KNIGHT, BLACK_BISHOP, BLACK_QUEEN,  BLACK_KING,   BLACK_BISHOP, BLACK_KNIGHT, BLACK_ROOK,
        BLACK_PAWN,   BLACK_PAWN,   BLACK_PAWN,   BLACK_PAWN,   BLACK_PAWN,   BLACK_PAWN,   BLACK_PAWN,   BLACK_PAWN,
        EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE,
        EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE,
        EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE,
        EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE,
        WHITE_PAWN,   WHITE_PAWN,   WHITE_PAWN,   WHITE_PAWN,   WHITE_PAWN,   WHITE_PAWN,   WHITE_PAWN,   WHITE_PAWN,
        WHITE_ROOK,   WHITE_KNIGHT, WHITE_BISHOP, WHITE_QUEEN,  WHITE_KING,   WHITE_BISHOP, WHITE_KNIGHT, WHITE_ROOK,
        # Whose turn it is (64):
        WHITE,
        # Castling rights: white kingside (65), white queenside (66), black kingside (67), black queenside (68):
        PRESENT, PRESENT, PRESENT, PRESENT,
        # En passant square position: row index (69), column index (70):
        NA, NA
    ],
    'vitalssSinceLastCaptureOrPawnMove': {(BLACK_ROOK, BLACK_KNIGHT, BLACK_BISHOP, BLACK_QUEEN, BLACK_KING, BLACK_BISHOP, BLACK_KNIGHT, BLACK_ROOK, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_ROOK, WHITE_KNIGHT, WHITE_BISHOP, WHITE_QUEEN, WHITE_KING, WHITE_BISHOP, WHITE_KNIGHT, WHITE_ROOK, WHITE, PRESENT, PRESENT, PRESENT, PRESENT, NA, NA): 1},
    'halfmovesSinceLastCaptureOrPawnMove': 0,
    'legalMoves': [((6, 6), (4, 6), None, -1), ((6, 2), (5, 2), None, -1), ((7, 6), (5, 5), None, -1), ((6, 6), (5, 6), None, -1), ((6, 1), (4, 1), None, -1), ((6, 3), (5, 3), None, -1), ((7, 6), (5, 7), None, -1), ((6, 2), (4, 2), None, -1), ((6, 3), (4, 3), None, -1), ((6, 7), (4, 7), None, -1), ((6, 5), (5, 5), None, -1), ((7, 1), (5, 0), None, -1), ((6, 7), (5, 7), None, -1), ((6, 0), (4, 0), None, -1), ((6, 1), (5, 1), None, -1), ((6, 4), (4, 4), None, -1), ((6, 0), (5, 0), None, -1), ((7, 1), (5, 2), None, -1), ((6, 5), (4, 5), None, -1), ((6, 4), (5, 4), None, -1)],
    'status': LIVE,
    'moveNumber': 1,
    'FEN': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
}
def getFreshGameState():
    return deepcopy(freshGameState)

def getOppositeColor(color):
    return BLACK if color == WHITE else WHITE


#####################################
# Conversion from game state to FEN:
#####################################

blackEncodedPieceToFENPiece = { PAWN: 'p', ROOK: 'r', KNIGHT: 'n', BISHOP: 'b', QUEEN: 'q', KING: 'k' }
whiteEncodedPieceToFENPiece = { PAWN: 'P', ROOK: 'R', KNIGHT: 'N', BISHOP: 'B', QUEEN: 'Q', KING: 'K' }
fenRows = ('8', '7', '6', '5', '4', '3', '2', '1')
fenColumns = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
encodedColorToFENColor = { WHITE: 'w', BLACK: 'b'}
def gameStateToFEN(vitals, halfmovesSinceLastCaptureOrPawnMove, moveNumber):
    res = ''
    for rowIndex in range(8):
        emptySquaresCount = 0
        for columnIndex in range(8):
            position = (rowIndex, columnIndex)
            if position not in vitals['pieces'][BLACK] and position not in vitals['pieces'][WHITE]:
                emptySquaresCount += 1
            else:
                if emptySquaresCount:
                    res += str(emptySquaresCount)
                    emptySquaresCount = 0
                if position in vitals['pieces'][BLACK]:
                    res += blackEncodedPieceToFENPiece[vitals['pieces'][BLACK][position]]
                else:
                    res += whiteEncodedPieceToFENPiece[vitals['pieces'][WHITE][position]]
        if emptySquaresCount:
            res += str(emptySquaresCount)
        if rowIndex != 7:
            res += '/'
    res += f" {encodedColorToFENColor[vitals['whoseTurnItIs']]} "
    castlingRights = ''
    for x in ((WHITE, 'K', 'Q'), (BLACK, 'k', 'q')):
        for y in ((KINGSIDE_CASTLING_RIGHT_INDEX, 1), (QUEENSIDE_CASTLING_RIGHT_INDEX, 2)):
            if vitals['castlingRights'][x[0]][y[0]] == PRESENT:
                castlingRights += x[y[1]]
    res += castlingRights if castlingRights else '-'
    res += f" {fenColumns[vitals['enPassantSquare'][1]]}{fenRows[vitals['enPassantSquare'][0]]} " if vitals['enPassantSquare'] else ' - '
    res += f'{halfmovesSinceLastCaptureOrPawnMove} {moveNumber}'
    return res


###########################################################################
# Conversion from FEN to feature vector (for processing imported dataset):
###########################################################################

FENPieceToEncodedPiece = { 'r': BLACK_ROOK, 'n': BLACK_KNIGHT, 'b': BLACK_BISHOP, 'q': BLACK_QUEEN, 'k': BLACK_KING, 'p': BLACK_PAWN, 'P': WHITE_PAWN, 'R': WHITE_ROOK, 'N': WHITE_KNIGHT, 'B': WHITE_BISHOP, 'Q': WHITE_QUEEN, 'K': WHITE_KING }
FENRowToRowIndex = { '8': ROW_8, '7': ROW_7, '6': ROW_6, '5': ROW_5, '4': ROW_4, '3': ROW_3, '2': ROW_2, '1': ROW_1 }
FENColToColIndex = { 'a': COLUMN_A, 'b': COLUMN_B, 'c': COLUMN_C, 'd': COLUMN_D, 'e': COLUMN_E, 'f': COLUMN_F, 'g': COLUMN_G, 'h': COLUMN_H }
def FENToFeatureVector(FEN):
    res = [EMPTY_SQUARE] * 71
    FENBoard, FENWhoseTurnItIs, FENCastlingRights, FENEnPassantSquare = FEN.split()[:4]
    index = 0
    for FENBoardChar in FENBoard:
        if FENBoardChar != '/':
            if FENBoardChar.isdigit():
                index += int(FENBoardChar)
            else:
                res[index] = FENPieceToEncodedPiece[FENBoardChar]
                index += 1
    res[64] = WHITE if FENWhoseTurnItIs == 'w' else BLACK
    res[65] = PRESENT if 'K' in FENCastlingRights else ABSENT
    res[66] = PRESENT if 'Q' in FENCastlingRights else ABSENT
    res[67] = PRESENT if 'k' in FENCastlingRights else ABSENT
    res[68] = PRESENT if 'q' in FENCastlingRights else ABSENT
    if FENEnPassantSquare != '-':
        res[69] = FENRowToRowIndex[FENEnPassantSquare[1]]
        res[70] = FENColToColIndex[FENEnPassantSquare[0]]
    else:
        res[69], res[70] = NA, NA
    return res


##########################################
# Calculating squares threatened by color:
##########################################

def isEmpty(position, pieces):
    return position not in pieces[BLACK] and position not in pieces[WHITE]

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

def squaresThreatenedByPawn(position, color):
    res = set()
    forwardRowIndexChange = 1 if color == BLACK else -1
    finalRowIndex = position[0] + forwardRowIndexChange
    for columnIndexBound, columnIndexChange in {(0, -1), (7, 1)}:
        if position[1] != columnIndexBound:
            res.add((finalRowIndex, position[1] + columnIndexChange))
    return res

def squaresThreatenedByPiece(piece, position, pieces, color):
    if piece == PAWN:
        return squaresThreatenedByPawn(position, color)
    elif piece == ROOK:
        return squaresThreatenedByRook(position, pieces)
    elif piece == KNIGHT:
        return squaresThreatenedByKnight(position)
    elif piece == BISHOP:
        return squaresThreatenedByBishop(position, pieces)
    elif piece == QUEEN:
        return squaresThreatenedByQueen(position, pieces)
    else:
        return squaresThreatenedByKing(position)

def squaresThreatenedByColor(pieces, color):
    res = set()
    for position, piece in pieces[color].items():
        res.update(squaresThreatenedByPiece(piece, position, pieces, color))
    return res


##########################
# Legal moves generation:
##########################

def isColorInCheck(oppositeColor, kingPosition, pieces):
    return kingPosition in squaresThreatenedByColor(pieces, oppositeColor)

# move: (initial position, final position, position of captured piece [or None if the move isn't a capture], type of piece to promote to [0-5, or -1 if the move isn't a pawn promotion])

def doesMoveLeaveKingInCheck(move, color, oppositeColor, kingPosition, pieces):
    pieces[color][move[1]] = pieces[color].pop(move[0])
    capturedPiece = pieces[oppositeColor].pop(move[2]) if move[2] else None
    res = isColorInCheck(oppositeColor, kingPosition, pieces)
    if capturedPiece != None:
        pieces[oppositeColor][move[2]] = capturedPiece
    pieces[color][move[0]] = pieces[color].pop(move[1])
    return res
    
def addMoveToResIfDoesntLeaveKingInCheck(res, move, color, oppositeColor, kingPosition, pieces):
    if not doesMoveLeaveKingInCheck(move, color, oppositeColor, kingPosition, pieces):
        res.add(move)

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
                    addMoveToResIfDoesntLeaveKingInCheck(res, (position, possibleAddition, possibleAddition, -1), color, oppositeColor, kingPosition, pieces)
                    break
                else:
                    addMoveToResIfDoesntLeaveKingInCheck(res, (position, possibleAddition, None, -1), color, oppositeColor, kingPosition, pieces)
                curPos[posIndexPointer] += positionChange
    return res

def hoppingPieceLegalMoveHelper(res, possibleMoveFinalPosition, possibleMoveInitialPosition, color, oppositeColor, kingPosition, pieces):
    if possibleMoveFinalPosition not in pieces[color]:
        if possibleMoveFinalPosition in pieces[oppositeColor]:
            addMoveToResIfDoesntLeaveKingInCheck(res, (possibleMoveInitialPosition, possibleMoveFinalPosition, possibleMoveFinalPosition, -1), color, oppositeColor, kingPosition, pieces)
        else:
            addMoveToResIfDoesntLeaveKingInCheck(res, (possibleMoveInitialPosition, possibleMoveFinalPosition, None, -1), color, oppositeColor, kingPosition, pieces)

def knightLegalMoves(position, color, oppositeColor, pieces, kingPosition):
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
                    addMoveToResIfDoesntLeaveKingInCheck(res, (position, possibleAddition, possibleAddition, -1), color, oppositeColor, kingPosition, pieces)
                    break
                else:
                    addMoveToResIfDoesntLeaveKingInCheck(res, (position, possibleAddition, None, -1), color, oppositeColor, kingPosition, pieces)
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
        castlingRowIndex = 0 if color == BLACK else 7
        if castlingRights[0] == PRESENT:
            squareOneToRightOfKing = (castlingRowIndex, 5)
            if isEmpty(squareOneToRightOfKing, pieces) and squareOneToRightOfKing not in squaresThreatenedByOpponent:
                squareTwoToRightOfKing = (castlingRowIndex, 6)
                if isEmpty(squareTwoToRightOfKing, pieces) and squareTwoToRightOfKing not in squaresThreatenedByOpponent:
                    res.add((position, squareTwoToRightOfKing, None, -1))
        if castlingRights[1] == PRESENT:
            squareOneToLeftOfKing = (castlingRowIndex, 3)
            if isEmpty(squareOneToLeftOfKing, pieces) and squareOneToLeftOfKing not in squaresThreatenedByOpponent:
                squareTwoToLeftOfKing = (castlingRowIndex, 2)
                if isEmpty(squareTwoToLeftOfKing, pieces) and squareTwoToLeftOfKing not in squaresThreatenedByOpponent and isEmpty((castlingRowIndex, 1), pieces):
                    res.add((position, squareTwoToLeftOfKing, None, -1))
    return res

def pawnLegalMoves(position, color, oppositeColor, pieces, kingPosition, enPassantSquare):
    res = set()
    if color == BLACK:
        doubleJumpStartingRowIndex = 1
        forwardRowIndexChange = 1
        promotionRowIndex = 7
    else:
        doubleJumpStartingRowIndex = 6
        forwardRowIndexChange = -1
        promotionRowIndex = 0
    singleHopFinalPosition = (position[0] + forwardRowIndexChange, position[1])
    if isEmpty(singleHopFinalPosition, pieces):

        possibleSingleJumpMove = (position, singleHopFinalPosition, None, -1)
        if not doesMoveLeaveKingInCheck(possibleSingleJumpMove, color, oppositeColor, kingPosition, pieces):
            if singleHopFinalPosition[0] == promotionRowIndex:
                for pieceType in {ROOK, KNIGHT, BISHOP, QUEEN}:
                    res.add((position, singleHopFinalPosition, None, pieceType))
            else:
                res.add(possibleSingleJumpMove)

        if position[0] == doubleJumpStartingRowIndex:
            doubleHopFinalPosition = (position[0] + 2 * forwardRowIndexChange, position[1])
            if isEmpty(doubleHopFinalPosition, pieces):
                addMoveToResIfDoesntLeaveKingInCheck(res, (position, doubleHopFinalPosition, None, -1), color, oppositeColor, kingPosition, pieces)
    for columnIndexChange, columnIndexBound in {(-1, 0), (1, 7)}:
        if position[1] != columnIndexBound:
            captureFinalPosition = (singleHopFinalPosition[0], position[1] + columnIndexChange)
            if captureFinalPosition in pieces[oppositeColor]:
                
                possibleRegularCaptureMove = (position, captureFinalPosition, captureFinalPosition, -1)
                if not doesMoveLeaveKingInCheck(possibleRegularCaptureMove, color, oppositeColor, kingPosition, pieces):
                    if captureFinalPosition[0] == promotionRowIndex:
                        for pieceType in {ROOK, KNIGHT, BISHOP, QUEEN}:
                            res.add((position, captureFinalPosition, captureFinalPosition, pieceType))
                    else:
                        res.add(possibleRegularCaptureMove)

            elif captureFinalPosition == enPassantSquare:
                addMoveToResIfDoesntLeaveKingInCheck(res, (position, captureFinalPosition, (position[0], captureFinalPosition[1]), -1), color, oppositeColor, kingPosition, pieces)
    return res

def pieceLegalMoves(piece, res, position, vitals, oppositeColor, kingPosition):
    if piece == PAWN:
        return pawnLegalMoves(position, vitals['whoseTurnItIs'], oppositeColor, vitals['pieces'], kingPosition, vitals['enPassantSquare'])
    elif piece == ROOK:
        return rookLegalMoves(position, vitals['whoseTurnItIs'], oppositeColor, vitals['pieces'], kingPosition)
    elif piece == KNIGHT:
        return knightLegalMoves(position, vitals['whoseTurnItIs'], oppositeColor, vitals['pieces'], kingPosition)
    elif piece == BISHOP:
        return bishopLegalMoves(position, vitals['whoseTurnItIs'], oppositeColor, vitals['pieces'], kingPosition)
    elif piece == QUEEN:
        return queenLegalMoves(position, vitals['whoseTurnItIs'], oppositeColor, vitals['pieces'], kingPosition)
    else:
        return kingLegalMoves(position, vitals['whoseTurnItIs'], oppositeColor, vitals['pieces'], vitals['castlingRights'][vitals['whoseTurnItIs']])

def legalMoves(vitals, kingPosition, oppositeColor):
    res = []
    for position, piece in vitals['pieces'][vitals['whoseTurnItIs']].copy().items():
        res.extend(pieceLegalMoves(piece, res, position, vitals, oppositeColor, kingPosition))
    return res


####################################
# Executing moves on the game state:
####################################

def squarePositionToFeatureVectorIndex(rowIndex, columnIndex):
    return rowIndex * 8 + columnIndex

def executeMove(move, gameState):
    if gameState['vitals']['whoseTurnItIs'] == BLACK:
        gameState['moveNumber'] += 1
        color = BLACK
        oppositeColor = WHITE
        pieceTypeToEncodedPiece = {
            ROOK: 0,
            KNIGHT: 1,
            BISHOP: 2,
            QUEEN: 3,
            KING: 4,
            PAWN: 5
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
        color = WHITE
        oppositeColor = BLACK
        pieceTypeToEncodedPiece = {
            PAWN: 7,
            ROOK: 8,
            KNIGHT: 9,
            BISHOP: 10,
            QUEEN: 11,
            KING: 12
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
    gameState['featureVector'][squarePositionToFeatureVectorIndex(move[0][0], move[0][1])] = EMPTY_SQUARE

    # Changing halfmovesSinceLastCaptureOrPawnMove: If the move is a capture or a pawn move, set to 0, otherwise increment by 1
    if move[2] or whatIsMoving == PAWN:
        gameState['halfmovesSinceLastCaptureOrPawnMove'] = 0
        gameState['vitalssSinceLastCaptureOrPawnMove'] = {}
    else:
        if gameState['halfmovesSinceLastCaptureOrPawnMove'] == 99:
            gameState['status'] = DRAW_BY_50_MOVE_RULE
            return
        gameState['halfmovesSinceLastCaptureOrPawnMove'] += 1

    # Changing board state: special cases = [castling, pawn promotion, en passant], default = move the piece
    # For castling, have to move the rook (the king is already moved later):
    if whatIsMoving == KING:
        gameState['kingPositions'][color] = move[1]
        for castlingRightIndex in {0, 1}:
            gameState['vitals']['castlingRights'][color][castlingRightIndex] = ABSENT
        for sideCastlingRightFeatureVectorIndex in {kingsideCastlingRightFeatureVectorIndex, queensideCastlingRightFeatureVectorIndex}:
            gameState['featureVector'][sideCastlingRightFeatureVectorIndex] = ABSENT
        if move == ((castlingRowIndex, 4), (castlingRowIndex, 6), None, -1):
            gameState['vitals']['pieces'][color].pop((castlingRowIndex, 7))
            gameState['featureVector'][squarePositionToFeatureVectorIndex(castlingRowIndex, 7)] = EMPTY_SQUARE
            gameState['vitals']['pieces'][color][(castlingRowIndex, 5)] = ROOK
            gameState['featureVector'][squarePositionToFeatureVectorIndex(castlingRowIndex, 5)] = pieceTypeToEncodedPiece[ROOK]
        elif move == ((castlingRowIndex, 4), (castlingRowIndex, 2), None, -1):
            gameState['vitals']['pieces'][color].pop((castlingRowIndex, 0))
            gameState['featureVector'][castlingRowIndex * 8] = EMPTY_SQUARE
            gameState['vitals']['pieces'][color][(castlingRowIndex, 3)] = ROOK
            gameState['featureVector'][squarePositionToFeatureVectorIndex(castlingRowIndex, 3)] = pieceTypeToEncodedPiece[ROOK]
    # Handling captures:
    if move[2]:
        gameState['vitals']['pieces'][oppositeColor].pop(move[2])
        gameState['featureVector'][squarePositionToFeatureVectorIndex(move[2][0], move[2][1])] = EMPTY_SQUARE
    
    if move[3] != -1:
        gameState['vitals']['pieces'][color][move[1]] = move[3]
        gameState['featureVector'][squarePositionToFeatureVectorIndex(move[1][0], move[1][1])] = pieceTypeToEncodedPiece[move[3]]
    else:
        gameState['vitals']['pieces'][color][move[1]] = whatIsMoving
        gameState['featureVector'][squarePositionToFeatureVectorIndex(move[1][0], move[1][1])] = pieceTypeToEncodedPiece[whatIsMoving]

    # Changing castling rights (we already handled the case where we move our king)
    # If you one of your rooks for the first time, need to modify your castling rights
    if move[0] == (castlingRowIndex, COLUMN_H):
        gameState['vitals']['castlingRights'][color][0] = ABSENT
        gameState['featureVector'][kingsideCastlingRightFeatureVectorIndex] = ABSENT
    elif move[0] == (castlingRowIndex, COLUMN_A):
        gameState['vitals']['castlingRights'][color][1] = ABSENT
        gameState['featureVector'][queensideCastlingRightFeatureVectorIndex] = ABSENT
    # If you capture one of your opponents rooks, possibly need to modify their castling rights
    if move[1] == (opponentCastlingRowIndex, COLUMN_A):
        gameState['vitals']['castlingRights'][oppositeColor][1] = ABSENT
        gameState['featureVector'][opponentQueensideCastlingRightFeatureVectorIndex] = ABSENT
    elif move[1] == (opponentCastlingRowIndex, COLUMN_H):
        gameState['vitals']['castlingRights'][oppositeColor][0] = ABSENT
        gameState['featureVector'][opponentKingsideCastlingRightFeatureVectorIndex] = ABSENT
    
    # Changing en passant square: If your move is a pawn double-jump, set the en passant square accordingly, otherwise set it to None
    if whatIsMoving == PAWN and move[0][0] == pawnDoubleJumpInitialRowIndex and move[1][0] == pawnDoubleJumpFinalRowIndex:
        gameState['vitals']['enPassantSquare'] = (newEnPassantSquareRowIndex, move[1][1])
        gameState['featureVector'][69], gameState['featureVector'][70] = newEnPassantSquareRowIndex, move[1][1]
    else:
        gameState['vitals']['enPassantSquare'] = None
        for enPassantSquareFeatureVectorIndex in {69, 70}:
            gameState['featureVector'][enPassantSquareFeatureVectorIndex] = NA
    
    # Check for draw by threefold repetition:
    # "Two positions are by definition 'the same' if the same types of pieces occupy the same squares, the same player 
    # has the move, the remaining castling rights are the same and the possibility to capture en passant is the same."
    vitals = tuple(gameState['featureVector'])
    if vitals in gameState['vitalssSinceLastCaptureOrPawnMove']:
        if gameState['vitalssSinceLastCaptureOrPawnMove'][vitals] == 2:
            gameState['status'] = DRAW_BY_THREEFOLD_REPETITION
            return
        gameState['vitalssSinceLastCaptureOrPawnMove'][vitals] += 1
    else:
        gameState['vitalssSinceLastCaptureOrPawnMove'][vitals] = 1

    # Check for draw by insufficient material:
    blackPieces = gameState['vitals']['pieces'][BLACK].values()
    whitePieces = gameState['vitals']['pieces'][WHITE].values()
    numPieces = len(blackPieces) + len(whitePieces)
    if numPieces == 4 and len(blackPieces) == 2 and len(whitePieces) == 2 and BISHOP in blackPieces and BISHOP in whitePieces:
        for position, piece in gameState['vitals']['pieces'][WHITE].items():
            if piece == BISHOP:
                whiteBishopPos = position
                break
        for position, piece in gameState['vitals']['pieces'][BLACK].items():
            if piece == BISHOP:
                blackBishopPos = position
                break
        if (whiteBishopPos[0] + whiteBishopPos[1]) % 2 == (blackBishopPos[0] + blackBishopPos[1]) % 2:
            gameState['status'] = DRAW_BY_INSUFFICIENT_MATERIAL
            return
    elif numPieces == 3:
        for pieceType in {KNIGHT, BISHOP}:
            for colorPieces in {blackPieces, whitePieces}:
                if pieceType in colorPieces:
                    gameState['status'] = DRAW_BY_INSUFFICIENT_MATERIAL
                    return
    elif numPieces == 2:
        gameState['status'] = DRAW_BY_INSUFFICIENT_MATERIAL
        return

    # Always change the active color to the opposite of what it currently is
    gameState['vitals']['whoseTurnItIs'] = oppositeColor
    gameState['featureVector'][64] = oppositeColor

    gameState['FEN'] = gameStateToFEN(gameState['vitals'], gameState['halfmovesSinceLastCaptureOrPawnMove'], gameState['moveNumber'])

    gameState['legalMoves'] = legalMoves(gameState['vitals'], gameState['kingPositions'][oppositeColor], color)

    if not gameState['legalMoves']:
        if isColorInCheck(color, gameState['kingPositions'][oppositeColor], gameState['vitals']['pieces']):
            gameState['status'] = CHECKMATE
        else:
            gameState['status'] = STALEMATE
        return