from copy import deepcopy

def fresh_game_state():
    board = [
        [-2, -3, -4, -5, -6, -4, -3, -2],
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [2, 3, 4, 5, 6, 4, 3, 2]
    ]
    active_color = [1]
    castling_rights = [1, 1, 1, 1]
    en_passant_square = [-1, -1]
    past_positions = [[square for row in board for square in row] + active_color + castling_rights + en_passant_square]
    pieces = {(i // 8, i % 8): past_positions[0][i] for i in range(64) if past_positions[0][i] != 0}
    return {
        'board': board,
        'active_color': active_color,
        'castling_rights': castling_rights,
        'en_passant_square': en_passant_square,
        'halfmoves_since_last_pawn_move_or_capture': [0],
        'past_positions': past_positions,
        'pieces': pieces,
        'legal_moves': legal_moves(board, active_color, castling_rights, en_passant_square, pieces),
        'status': ['live']
    }

def is_valid_square(pos):
    return 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7

def is_color(color, pos, board):
    if not is_valid_square(pos):
        return False
    piece = board[pos[0]][pos[1]]
    if color == 1:
        return board[pos[0]][pos[1]] > 0
    return board[pos[0]][pos[1]] < 0

def is_empty(pos, board):
    return is_valid_square(pos) and board[pos[0]][pos[1]] == 0

def squares_threatened_by_sliding_piece(directions, pos, board):
    res = []
    for direction in directions:
        distance = 1
        while True:
            if is_valid_square([pos[0] + direction[0] * distance, pos[1] + direction[1] * distance]):
                res.append([pos[0] + direction[0] * distance, pos[1] + direction[1] * distance])
            else:
                break
            if board[pos[0] + direction[0] * distance][pos[1] + direction[1] * distance] != 0:
                break
            distance += 1
    return res

def squares_threatened_by_hopping_piece(movements, pos):
    res = []
    for movement in movements:
        possible_addition = [pos[0] + movement[0], pos[1] + movement[1]]
        if is_valid_square(possible_addition):
            res.append(possible_addition)
    return res

def squares_threatened_by_pawn(color, pos):
    res = []
    if color == 1:
        row_index_change_for_forward = -1
    else:
        row_index_change_for_forward = 1
    for i in [-1, 1]:
        possible_addition = [pos[0] + row_index_change_for_forward, pos[1] + i]
        if is_valid_square(possible_addition):
            res.append(possible_addition)
    return res

def squares_threatened_by_piece(color, pos, board):
    type_ = abs(board[pos[0]][pos[1]])
    if type_ == 1:
        return squares_threatened_by_pawn(color, pos)
    elif type_ == 2:
        return squares_threatened_by_sliding_piece([[-1, 0], [0, 1], [1, 0], [0, -1]], pos, board)
    elif type_ == 3:
        return squares_threatened_by_hopping_piece([[-2, 1], [-1, 2], [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1]], pos)
    elif type_ == 4:
        return squares_threatened_by_sliding_piece([[-1, 1], [1, 1], [1, -1], [-1, -1]], pos, board)
    elif type_ == 5:
        return squares_threatened_by_sliding_piece([[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]], pos, board)
    else:
        return squares_threatened_by_hopping_piece([[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]], pos)

def squares_threatened_by_color(color, board):
    res = []
    for i in range(8):
        for j in range(8):
            if is_color(color, [i, j], board):
                res += squares_threatened_by_piece(color, [i, j], board)
    return res

def move_piece(pos_i, pos_f, board, pieces):
    pieces[tuple(pos_f)] = board[pos_i[0]][pos_i[1]]
    board[pos_f[0]][pos_f[1]] = board[pos_i[0]][pos_i[1]]
    pieces.pop(tuple(pos_i))
    board[pos_i[0]][pos_i[1]] = 0

def execute_move_just_for_checking_legality(move, board, active_color, castling_rights, en_passant_square, pieces):
    pos_i, pos_f = move[0], move[1]
    what_is_at_pos_i = board[pos_i[0]][pos_i[1]]
    if active_color[0] == 1:
        castling_row_index = 7
        kingside_castling_right_index = 0
        queenside_castling_right_index = 1
        row_index_change_for_backward = 1
        pawn = 1
        promotion_row_index = 0
        queen = 5
    else:
        castling_row_index = 0
        kingside_castling_right_index = 2
        queenside_castling_right_index = 3
        row_index_change_for_backward = -1
        pawn = -1
        promotion_row_index = 7
        queen = -5
    # Changing board state: special cases = [castling, pawn promotion, en passant], default = move the piece
    # Default:
    move_piece(pos_i, pos_f, board, pieces)
    # Pawn promotion (automatically promote to queen for now for simplicity)
    if board[pos_f[0]][pos_f[1]] == pawn and pos_f[0] == promotion_row_index:
        pieces[tuple(pos_f)] = queen
        board[pos_f[0]][pos_f[1]] = queen
    # Castling:
    if move == [[castling_row_index, 4], [castling_row_index, 6]] and castling_rights[kingside_castling_right_index]:
        move_piece([castling_row_index, 7], [castling_row_index, 5], board, pieces)
    elif move == [[castling_row_index, 4], [castling_row_index, 2]] and castling_rights[queenside_castling_right_index]:
        move_piece([castling_row_index, 0], [castling_row_index, 3], board, pieces)
    # En passant:
    if pos_f == en_passant_square and what_is_at_pos_i == pawn:
        pieces.pop((pos_f[0] + row_index_change_for_backward, pos_f[1]))
        board[pos_f[0] + row_index_change_for_backward][pos_f[1]] = 0

def execute_move(move, game_state):
    move = [list(move[0]), list(move[1])]
    pos_i, pos_f = move[0], move[1]

    if game_state['active_color'][0] == 1:
        opponents_pieces = range(-1, -7, -1)
        pawn = 1
        opponent_pawn = -1
        queen = 5
        promotion_row_index = 0
        castling_row_index = 7
        opponent_castling_row_index = 0
        kingside_castling_right_index = 0
        queenside_castling_right_index = 1
        opponent_kingside_castling_right_index = 2
        opponent_queenside_castling_right_index = 3
        pawn_double_jump_row_index_i = 6
        pawn_double_jump_row_index_f = 4
        new_en_passant_square_row_index = 5
        row_index_change_for_backward = 1
    else:
        opponents_pieces = range(1, 7)
        pawn = -1
        opponent_pawn = 1
        queen = -5
        promotion_row_index = 7
        castling_row_index = 0
        opponent_castling_row_index = 7
        kingside_castling_right_index = 2
        queenside_castling_right_index = 3
        opponent_kingside_castling_right_index = 0
        opponent_queenside_castling_right_index = 1
        pawn_double_jump_row_index_i = 1
        pawn_double_jump_row_index_f = 3
        new_en_passant_square_row_index = 2
        row_index_change_for_backward = -1

    # Changing halfmoves_since_last_pawn_move_or_capture: If the move is a capture or a pawn move, set to 0, otherwise increment by 1
    what_is_at_pos_i = game_state['board'][pos_i[0]][pos_i[1]]
    what_is_at_pos_f = game_state['board'][pos_f[0]][pos_f[1]]
    if what_is_at_pos_f in opponents_pieces or (what_is_at_pos_i == pawn and pos_f == game_state['en_passant_square']):
        game_state['past_positions'] = []
        game_state['halfmoves_since_last_pawn_move_or_capture'][0] = 0
    else:
        game_state['halfmoves_since_last_pawn_move_or_capture'][0] += 1
        # Check for draw by fifty-move rule:
        if game_state['halfmoves_since_last_pawn_move_or_capture'][0] == 50:
            game_state['status'][0] = 'Draw by fifty-move rule'
            return

    execute_move_just_for_checking_legality(move, game_state['board'], game_state['active_color'], game_state['castling_rights'], game_state['en_passant_square'], game_state['pieces'])

    # Changing castling rights: if you move your king or one of your rooks for the first time, or if you capture one of your opponents rooks
    if pos_i == [castling_row_index, 4]:
        if game_state['castling_rights'][kingside_castling_right_index]:
            game_state['castling_rights'][kingside_castling_right_index] = 0
        if game_state['castling_rights'][queenside_castling_right_index]:
            game_state['castling_rights'][queenside_castling_right_index] = 0
    elif pos_i == [castling_row_index, 7] and game_state['castling_rights'][kingside_castling_right_index]:
        game_state['castling_rights'][kingside_castling_right_index] = 0
    elif pos_i == [castling_row_index, 0] and game_state['castling_rights'][queenside_castling_right_index]:
        game_state['castling_rights'][queenside_castling_right_index] = 0
    if pos_f == [opponent_castling_row_index, 0] and game_state['castling_rights'][opponent_queenside_castling_right_index]:
        game_state['castling_rights'][opponent_queenside_castling_right_index] = 0
    elif pos_f == [opponent_castling_row_index, 7] and game_state['castling_rights'][opponent_kingside_castling_right_index]:
        game_state['castling_rights'][opponent_kingside_castling_right_index] = 0

    # # Update castling rights when king moves
    # if what_is_at_pos_i == 6 or what_is_at_pos_i == -6:  # King moved
    #     game_state['castling_rights'][kingside_castling_right_index] = 0
    #     game_state['castling_rights'][queenside_castling_right_index] = 0

    # # Update castling rights when rook moves
    # if what_is_at_pos_i == 2 or what_is_at_pos_i == -2:  # Rook moved
    #     if pos_i == [castling_row_index, 7]:  # Kingside rook
    #         game_state['castling_rights'][kingside_castling_right_index] = 0
    #     elif pos_i == [castling_row_index, 0]:  # Queenside rook
    #         game_state['castling_rights'][queenside_castling_right_index] = 0

    # # Update opponent's castling rights when their rook is captured
    # if what_is_at_pos_f == -2 and pos_f == [opponent_castling_row_index, 7]:
    #     game_state['castling_rights'][opponent_kingside_castling_right_index] = 0
    # elif what_is_at_pos_f == -2 and pos_f == [opponent_castling_row_index, 0]:
    #     game_state['castling_rights'][opponent_queenside_castling_right_index] = 0
    
    # Changing en passant square: If your move is a pawn double-jump, set the en passant square accordingly, else set it to None
    if game_state['board'][pos_f[0]][pos_f[1]] == pawn and pos_f[0] == pawn_double_jump_row_index_f and pos_i[0] == pawn_double_jump_row_index_i:
        game_state['en_passant_square'] = [new_en_passant_square_row_index, pos_f[1]]
    else:
        game_state['en_passant_square'] = [-1, -1]
    
    # Check for draw by threefold repetition:
    # "Two positions are by definition 'the same' if the same types of pieces occupy the same squares, the same player has the move, 
    # the remaining castling rights are the same and the possibility to capture en passant is the same."
    position = [square for row in game_state['board'] for square in row] + game_state['active_color'] + game_state['castling_rights'] + game_state['en_passant_square']
    if game_state['past_positions'].count(position) == 2:
        game_state['status'][0] = 'Draw by threefold repetition'
        return
    game_state['past_positions'].append(position)

    # Check for draw by insufficient material:
    if len(game_state['pieces']) == 4 and 4 in game_state['pieces'].values() and -4 in game_state['pieces'].values():
        white_bishop_pos = None
        black_bishop_pos = None
        for pos, piece in game_state['pieces'].items():
            if piece == 4:
                white_bishop_pos = pos
                if black_bishop_pos:
                    break
            elif piece == -4:
                black_bishop_pos = pos
                if white_bishop_pos:
                    break
        if (white_bishop_pos[0] + white_bishop_pos[1]) % 2 == (black_bishop_pos[0] + black_bishop_pos[1]) % 2:
            game_state['status'][0] = 'Draw by insufficient material'
            return
    elif len(game_state['pieces']) == 3:
        for piece in [3, 4, -3, -4]:
            if piece in game_state['pieces'].values():
                game_state['status'][0] = 'Draw by insufficient material'
                return
    elif len(game_state['pieces']) == 2:
        game_state['status'][0] = 'Draw by insufficient material'
        return

    # Always change the active color to the opposite of what it currently is
    game_state['active_color'][0] *= -1
    
    game_state['legal_moves'] = legal_moves(game_state['board'], game_state['active_color'], game_state['castling_rights'], game_state['en_passant_square'], game_state['pieces'])
   
    if len(game_state['legal_moves']) == 0:
        if is_player_in_check(game_state['active_color'][0], game_state['board']):
            if game_state['active_color'][0] == 1:
                game_state['status'][0] = 'Black checkmates white.'
            else:
                game_state['status'][0] = 'White checkmates black.'
        else:
            if game_state['active_color'][0] == 1:
                game_state['status'][0] = 'Black stalemates white.'
            else:
                game_state['status'][0] = 'White stalemates black.'

def is_player_in_check(color, board):
    squares_threatened_by_opponent = squares_threatened_by_color(color * -1, board)
    if color == 1:
        king = 6
    else:
        king = -6
    for square in squares_threatened_by_opponent:
        if board[square[0]][square[1]] == king:
            return True
    return False

def move_doesnt_leave_king_in_check(move, board, active_color, castling_rights, en_passant_square, pieces):
    board_copy = deepcopy(board)
    pieces_copy = deepcopy(pieces)
    execute_move_just_for_checking_legality(move, board_copy, active_color, castling_rights, en_passant_square, pieces_copy)
    if is_player_in_check(active_color[0], board_copy):
        return False
    return True

def append_move_to_res_if_doesnt_leave_king_in_check(res, move, board, active_color, castling_rights, en_passant_square, pieces):
    if move_doesnt_leave_king_in_check(move, board, active_color, castling_rights, en_passant_square, pieces):
        res.append(move)

def sliding_piece_legal_moves(directions, pos, board, active_color, castling_rights, en_passant_square, pieces):
    res = []
    for direction in directions:
        distance = 1
        while True:
            if is_empty([pos[0] + direction[0] * distance, pos[1] + direction[1] * distance], board) or is_color(active_color[0] * -1, [pos[0] + direction[0] * distance, pos[1] + direction[1] * distance], board):
                append_move_to_res_if_doesnt_leave_king_in_check(res, [pos, [pos[0] + direction[0] * distance, pos[1] + direction[1] * distance]], board, active_color, castling_rights, en_passant_square, pieces)
            else:
                break
            if is_color(active_color[0] * -1, [pos[0] + direction[0] * distance, pos[1] + direction[1] * distance], board):
                break
            distance += 1
    return res

def hopping_piece_legal_moves(movements, pos, board, active_color, castling_rights, en_passant_square, pieces):
    res = []
    for movement in movements:
        possible_addition = [pos[0] + movement[0], pos[1] + movement[1]]
        if is_empty(possible_addition, board) or is_color(active_color[0] * -1, possible_addition, board):
            append_move_to_res_if_doesnt_leave_king_in_check(res, [pos, possible_addition], board, active_color, castling_rights, en_passant_square, pieces)
    return res

def pawn_legal_moves(pos, board, active_color, castling_rights, en_passant_square, pieces):
    res = []
    if active_color[0] == 1:
        double_jump_row_index = 6
        change_row_index_for_forward = -1
    else:
        double_jump_row_index = 1
        change_row_index_for_forward = 1
    if is_empty([pos[0] + change_row_index_for_forward, pos[1]], board):
        append_move_to_res_if_doesnt_leave_king_in_check(res, [pos, [pos[0] + change_row_index_for_forward, pos[1]]], board, active_color, castling_rights, en_passant_square, pieces)
        if pos[0] == double_jump_row_index and is_empty([pos[0] + change_row_index_for_forward * 2, pos[1]], board):
            append_move_to_res_if_doesnt_leave_king_in_check(res, [pos, [pos[0] + change_row_index_for_forward * 2, pos[1]]], board, active_color, castling_rights, en_passant_square, pieces)
    for i in [-1, 1]:
        if is_color(active_color[0] * -1, [pos[0] + change_row_index_for_forward, pos[1] + i], board) or [pos[0] + change_row_index_for_forward, pos[1] + i] == en_passant_square:
            append_move_to_res_if_doesnt_leave_king_in_check(res, [pos, [pos[0] + change_row_index_for_forward, pos[1] + i]], board, active_color, castling_rights, en_passant_square, pieces)
    return res

def rook_legal_moves(pos, board, active_color, castling_rights, en_passant_square, pieces):
    return sliding_piece_legal_moves([[-1, 0], [0, 1], [1, 0], [0, -1]], pos, board, active_color, castling_rights, en_passant_square, pieces)

def bishop_legal_moves(pos, board, active_color, castling_rights, en_passant_square, pieces):
    return sliding_piece_legal_moves([[-1, 1], [1, 1], [1, -1], [-1, -1]], pos, board, active_color, castling_rights, en_passant_square, pieces)

def queen_legal_moves(pos, board, active_color, castling_rights, en_passant_square, pieces):
    return sliding_piece_legal_moves([[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]], pos, board, active_color, castling_rights, en_passant_square, pieces)

def knight_legal_moves(pos, board, active_color, castling_rights, en_passant_square, pieces):
    return hopping_piece_legal_moves([[-2, 1], [-1, 2], [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1]], pos, board, active_color, castling_rights, en_passant_square, pieces)

def king_legal_moves(pos, board, active_color, castling_rights, en_passant_square, pieces):
    res = []
    squares_threatened_by_opponent = squares_threatened_by_color(active_color[0] * -1, board)
    if active_color[0] == 1:
        if (
            castling_rights[0] and
            is_empty([7, 5], board) and
            is_empty([7, 6], board) and
            [7, 5] not in squares_threatened_by_opponent
        ):
            append_move_to_res_if_doesnt_leave_king_in_check(res, [[7, 4], [7, 6]], board, active_color, castling_rights, en_passant_square, pieces)
        if (
            castling_rights[1] and
            is_empty([7, 3], board) and
            is_empty([7, 2], board) and
            is_empty([7, 1], board) and
            [7, 3] not in squares_threatened_by_opponent
        ):
            append_move_to_res_if_doesnt_leave_king_in_check(res, [[7,4], [7,2]], board, active_color, castling_rights, en_passant_square, pieces)
    else:
        if (
            castling_rights[2] and
            is_empty([0, 5], board) and
            is_empty([0, 6], board) and
            [0, 5] not in squares_threatened_by_opponent
        ):
            append_move_to_res_if_doesnt_leave_king_in_check(res, [[0, 4], [0, 6]], board, active_color, castling_rights, en_passant_square, pieces)
        if (
            castling_rights[3] and
            is_empty([0, 3], board) and
            is_empty([0, 2], board) and
            is_empty([0, 1], board) and
            [0, 3] not in squares_threatened_by_opponent
        ):
            append_move_to_res_if_doesnt_leave_king_in_check(res, [[0, 4], [0, 2]], board, active_color, castling_rights, en_passant_square, pieces)
    return hopping_piece_legal_moves([[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]], pos, board, active_color, castling_rights, en_passant_square, pieces) + res

type_legal_moves = {
    1: pawn_legal_moves,
    2: rook_legal_moves,
    3: knight_legal_moves,
    4: bishop_legal_moves,
    5: queen_legal_moves,
    6: king_legal_moves
}

def piece_legal_moves(pos, board, active_color, castling_rights, en_passant_square, pieces):
    return type_legal_moves[abs(board[pos[0]][pos[1]])](pos, board, active_color, castling_rights, en_passant_square, pieces)

def legal_moves(board, active_color, castling_rights, en_passant_square, pieces):
    res = []
    for i in range(8):
        for j in range(8):
            if is_color(active_color[0], [i, j], board):
                res += piece_legal_moves([i, j], board, active_color, castling_rights, en_passant_square, pieces)
    return res

# For testing:
piece_symbols = {
    1: '♙', 2: '♖', 3: '♘', 4: '♗', 5: '♕', 6: '♔',
    -1: '♟', -2: '♜', -3: '♞', -4: '♝', -5: '♛', -6: '♚',
    0: '·'
}
def print_chess_board(board):
    for row in board:
        row_str = ''.join([piece_symbols[piece] + ' ' for piece in row])
        print(row_str)
    print()