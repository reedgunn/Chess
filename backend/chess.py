from collections import defaultdict

def get_fresh_game_state():
    return {
        'feature_vector': [-2, -3, -4, -5, -6, -4, -3, -2, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 6, 4, 3, 2, 1, 1, 1, 1, 1, -1, -1],
        'halfmoves_since_last_pawn_move_or_capture': 0,
        'move_number': 1,
        'FEN': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
        'pieces': {
            1: {
                (6, 0):  1, (6, 1):  1, (6, 2):  1, (6, 3):  1, (6, 4):  1, (6, 5):  1, (6, 6):  1, (6, 7):  1,
                (7, 0):  2, (7, 1):  3, (7, 2):  4, (7, 3):  5, (7, 4):  6, (7, 5):  4, (7, 6):  3, (7, 7):  2
            },
            -1: {
                (0, 0): -2, (0, 1): -3, (0, 2): -4, (0, 3): -5, (0, 4): -6, (0, 5): -4, (0, 6): -3, (0, 7): -2,
                (1, 0): -1, (1, 1): -1, (1, 2): -1, (1, 3): -1, (1, 4): -1, (1, 5): -1, (1, 6): -1, (1, 7): -1
            }
        },
        'king_positions': {
            1: (7, 4), -1: (0, 4)
        },
        'past_positions': defaultdict(int, {(-2, -3, -4, -5, -6, -4, -3, -2, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 6, 4, 3, 2, 1, 1, 1, 1, 1, -1, -1): 1}),
        'legal_moves': {
            ((6, 0), (5, 0), None), ((6, 0), (4, 0), None), ((6, 1), (5, 1), None), ((6, 1), (4, 1), None), ((6, 2), (5, 2), None), ((6, 2), (4, 2), None), ((6, 3), (5, 3), None), 
            ((6, 3), (4, 3), None), ((6, 4), (5, 4), None), ((6, 4), (4, 4), None), ((6, 5), (5, 5), None), ((6, 5), (4, 5), None), ((6, 6), (5, 6), None), ((6, 6), (4, 6), None), 
            ((6, 7), (5, 7), None), ((6, 7), (4, 7), None), ((7, 1), (5, 2), None), ((7, 1), (5, 0), None), ((7, 6), (5, 7), None), ((7, 6), (5, 5), None)
        },
        'status': 'live'
    }

int_piece_to_FEN_piece = {
    1: 'P', 2: 'R', 3: 'N', 4: 'B', 5: 'Q', 6: 'K',
    -1: 'p', -2: 'r', -3: 'n', -4: 'b', -5: 'q', -6: 'k'
}
FEN_castling_rights = ('K', 'Q', 'k', 'q')
FEN_rows = ('8', '7', '6', '5', '4', '3', '2', '1')
FEN_columns = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
def get_FEN(feature_vector, halfmoves_since_last_pawn_move_or_capture, move_number):
    res = ''
    for i in range(0, 64, 8):
        empty_squares_count = 0
        for j in range(i, i + 8, 1):
            whats_at_square = feature_vector[j]
            if not whats_at_square:
                empty_squares_count += 1
            else:
                if empty_squares_count:
                    res += str(empty_squares_count)
                    empty_squares_count = 0
                res += int_piece_to_FEN_piece[whats_at_square]
        if empty_squares_count:
            res += str(empty_squares_count)
        if i != 56:
            res += '/'
    res += ' w ' if feature_vector[64] == 1 else ' b '
    castling_rights = ''
    for i in range(4):
        if feature_vector[65 + i]:
            castling_rights += FEN_castling_rights[i]
    res += f'{castling_rights} ' if castling_rights else '- '
    if feature_vector[69] == -1:
        res += '-'
    else:
        res += FEN_columns[feature_vector[70]] + FEN_rows[feature_vector[69]]
    res += f' {halfmoves_since_last_pawn_move_or_capture} {move_number}'
    return res

ACTIVE_COLOR_FV_INDEX = 64
WHITE_KINGSIDE_CASTLING_RIGHT_FV_INDEX = 65
WHITE_QUEENSIDE_CASTLING_RIGHT_FV_INDEX = 66
BLACK_KINGSIDE_CASTLING_RIGHT_FV_INDEX = 67
BLACK_QUEENSIDE_CASTLING_RIGHT_FV_INDEX = 68
EN_PASSANT_SQUARE_ROW_INDEX_FV_INDEX = 69
EN_PASSANT_SQUARE_COLUMN_INDEX_FV_INDEX = 70

opposite_colors = {1: -1, -1: 1}
def get_opposite_color(color):
    return opposite_colors[color]

def is_empty(pos, pieces):
    return pos not in pieces[1] and pos not in pieces[-1]

def squares_threatened_by_pawn(pos, color):
    res = set()
    res_row_index, col_index = pos[0] - color, pos[1]
    if col_index != 0:
        res.add((res_row_index, col_index - 1))
    if col_index != 7:
        res.add((res_row_index, col_index + 1))
    return res

def squares_threatened_by_rook(pos, pieces):
    res = set()
    row_index, col_index = pos
    # Sliding north:
    cur_pos = [row_index - 1, col_index]
    while cur_pos[0] != -1:
        addition = tuple(cur_pos)
        res.add(addition)
        if addition in pieces[1] or addition in pieces[-1]:
            break
        cur_pos[0] -= 1
    # Sliding east:
    cur_pos = [row_index, col_index + 1]
    while cur_pos[1] != 8:
        addition = tuple(cur_pos)
        res.add(addition)
        if addition in pieces[1] or addition in pieces[-1]:
            break
        cur_pos[1] += 1
    # Sliding south:
    cur_pos = [row_index + 1, col_index]
    while cur_pos[0] != 8:
        addition = tuple(cur_pos)
        res.add(addition)
        if addition in pieces[1] or addition in pieces[-1]:
            break
        cur_pos[0] += 1
    # Sliding west:
    cur_pos = [row_index, col_index - 1]
    while cur_pos[1] != -1:
        addition = tuple(cur_pos)
        res.add(addition)
        if addition in pieces[1] or addition in pieces[-1]:
            break
        cur_pos[1] -= 1
    #
    return res

def squares_threatened_by_knight(pos):
    res = set()
    row_index, col_index = pos
    not_on_top_edge = row_index != 0
    not_close_to_top_edge = not_on_top_edge and row_index != 1
    not_on_right_edge = col_index != 7
    not_close_to_right_edge = not_on_right_edge and col_index != 6
    not_on_bottom_edge = row_index != 7
    not_close_to_bottom_edge = not_on_bottom_edge and row_index != 6
    not_on_left_edge = col_index != 0
    not_close_to_left_edge = not_on_left_edge and col_index != 1
    # Big up
    if not_close_to_top_edge:
        # Small left
        if not_on_left_edge:
            res.add((row_index - 2, col_index - 1))
        # Small right
        if not_on_right_edge:
            res.add((row_index - 2, col_index + 1))
    # Big right
    if not_close_to_right_edge:
        # Small up
        if not_on_top_edge:
            res.add((row_index - 1, col_index + 2))
        # Small down
        if not_on_bottom_edge:
            res.add((row_index + 1, col_index + 2))
    # Big down
    if not_close_to_bottom_edge:
        # Small right
        if not_on_right_edge:
            res.add((row_index + 2, col_index + 1))
        # Small left
        if not_on_left_edge:
            res.add((row_index + 2, col_index - 1))
    # Big left
    if not_close_to_left_edge:
        # Small down
        if not_on_bottom_edge:
            res.add((row_index + 1, col_index - 2))
        # Small up
        if not_on_top_edge:
            res.add((row_index - 1, col_index - 2))
    #
    return res

def squares_threatened_by_bishop(pos, pieces):
    res = set()
    row_index, col_index = pos
    # Sliding northeast:
    cur_pos = [row_index - 1, col_index + 1]
    while cur_pos[0] != -1 and cur_pos[1] != 8:
        addition = tuple(cur_pos)
        res.add(addition)
        if addition in pieces[1] or addition in pieces[-1]:
            break
        cur_pos[0] -= 1
        cur_pos[1] += 1
    # Sliding southeast:
    cur_pos = [row_index + 1, col_index + 1]
    while cur_pos[0] != 8 and cur_pos[1] != 8:
        addition = tuple(cur_pos)
        res.add(addition)
        if addition in pieces[1] or addition in pieces[-1]:
            break
        cur_pos[0] += 1
        cur_pos[1] += 1
    # Sliding southwest:
    cur_pos = [row_index + 1, col_index - 1]
    while cur_pos[0] != 8 and cur_pos[1] != -1:
        addition = tuple(cur_pos)
        res.add(addition)
        if addition in pieces[1] or addition in pieces[-1]:
            break
        cur_pos[0] += 1
        cur_pos[1] -= 1
    # Sliding northwest:
    cur_pos = [row_index - 1, col_index - 1]
    while cur_pos[0] != -1 and cur_pos[1] != -1:
        addition = tuple(cur_pos)
        res.add(addition)
        if addition in pieces[1] or addition in pieces[-1]:
            break
        cur_pos[0] -= 1
        cur_pos[1] -= 1
    #
    return res

def squares_threatened_by_queen(pos, pieces):
    res = set()
    row_index, col_index = pos
    # Sliding north:
    cur_pos = [row_index - 1, col_index]
    while cur_pos[0] != -1:
        addition = tuple(cur_pos)
        res.add(addition)
        if addition in pieces[1] or addition in pieces[-1]:
            break
        cur_pos[0] -= 1
    # Sliding northeast:
    cur_pos = [row_index - 1, col_index + 1]
    while cur_pos[0] != -1 and cur_pos[1] != 8:
        addition = tuple(cur_pos)
        res.add(addition)
        if addition in pieces[1] or addition in pieces[-1]:
            break
        cur_pos[0] -= 1
        cur_pos[1] += 1
    # Sliding east:
    cur_pos = [row_index, col_index + 1]
    while cur_pos[1] != 8:
        addition = tuple(cur_pos)
        res.add(addition)
        if addition in pieces[1] or addition in pieces[-1]:
            break
        cur_pos[1] += 1
    # Sliding southeast:
    cur_pos = [row_index + 1, col_index + 1]
    while cur_pos[0] != 8 and cur_pos[1] != 8:
        addition = tuple(cur_pos)
        res.add(addition)
        if addition in pieces[1] or addition in pieces[-1]:
            break
        cur_pos[0] += 1
        cur_pos[1] += 1
    # Sliding south:
    cur_pos = [row_index + 1, col_index]
    while cur_pos[0] != 8:
        addition = tuple(cur_pos)
        res.add(addition)
        if addition in pieces[1] or addition in pieces[-1]:
            break
        cur_pos[0] += 1
    # Sliding southwest:
    cur_pos = [row_index + 1, col_index - 1]
    while cur_pos[0] != 8 and cur_pos[1] != -1:
        addition = tuple(cur_pos)
        res.add(addition)
        if addition in pieces[1] or addition in pieces[-1]:
            break
        cur_pos[0] += 1
        cur_pos[1] -= 1
    # Sliding west:
    cur_pos = [row_index, col_index - 1]
    while cur_pos[1] != -1:
        addition = tuple(cur_pos)
        res.add(addition)
        if addition in pieces[1] or addition in pieces[-1]:
            break
        cur_pos[1] -= 1
    # Sliding northwest:
    cur_pos = [row_index - 1, col_index - 1]
    while cur_pos[0] != -1 and cur_pos[1] != -1:
        addition = tuple(cur_pos)
        res.add(addition)
        if addition in pieces[1] or addition in pieces[-1]:
            break
        cur_pos[0] -= 1
        cur_pos[1] -= 1
    #
    return res

def squares_threatened_by_king(pos):
    res = set()
    row_index, col_index = pos
    not_on_top_edge = row_index != 0
    not_on_right_edge = col_index != 7
    not_on_bottom_edge = row_index != 7
    not_on_left_edge = col_index != 0
    # North:
    if not_on_top_edge:
        res.add((row_index - 1, col_index))
        # Northeast:
        if not_on_right_edge:
            res.add((row_index - 1, col_index + 1))
        # Northwest:
        if not_on_left_edge:
            res.add((row_index - 1, col_index - 1))
    # South
    if not_on_bottom_edge:
        res.add((row_index + 1, col_index))
        # Southeast:
        if not_on_right_edge:
            res.add((row_index + 1, col_index + 1))
        # Southwest:
        if not_on_left_edge:
            res.add((row_index + 1, col_index - 1))
    # East:
    if not_on_right_edge:
        res.add((row_index, col_index + 1))
    # West:
    if not_on_left_edge:
        res.add((row_index, col_index - 1))
    #
    return res

def squares_threatened_by_color(color, pieces):
    res = set()
    for pos, piece in pieces[color].items():
        piece_type = piece * color
        if piece_type == 1:
            res.update(squares_threatened_by_pawn(pos, color))
        elif piece_type == 2:
            res.update(squares_threatened_by_rook(pos, pieces))
        elif piece_type == 3:
            res.update(squares_threatened_by_knight(pos))
        elif piece_type == 4:
            res.update(squares_threatened_by_bishop(pos, pieces))
        elif piece_type == 5:
            res.update(squares_threatened_by_queen(pos, pieces))
        else:
            res.update(squares_threatened_by_king(pos))
    return res

def is_color_in_check(opposite_color, king_position, pieces):
    return king_position in squares_threatened_by_color(opposite_color, pieces)

def does_move_leave_king_in_check(move, color, king_position, pieces):
    pos_i, pos_f, pos_captured_piece = move
    opposite_color = get_opposite_color(color)
    piece_to_move = pieces[color].pop(pos_i)
    piece_to_capture = pieces[opposite_color].pop(pos_captured_piece) if pos_captured_piece else None
    pieces[color][pos_f] = color
    res = is_color_in_check(opposite_color, king_position, pieces)
    if piece_to_capture:
        pieces[opposite_color][pos_captured_piece] = piece_to_capture
    pieces[color][pos_i] = piece_to_move
    pieces[color].pop(pos_f)
    return res
    
def add_move_to_res_if_doesnt_leave_king_in_check(res, move, color, king_position, pieces):
    if not does_move_leave_king_in_check(move, color, king_position, pieces):
        res.add(move)

# move vector: (initial position, final_position, position of piece to capture (or None if move isn't a capture))
    
def helper(res, pos, possible_addition, pieces, color, opposite_color, king_position):
    if possible_addition not in pieces[color]:
        if possible_addition in pieces[opposite_color]:
            add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, possible_addition), color, king_position, pieces)
        else:
            add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, None), color, king_position, pieces)

def pawn_legal_moves(pos, color, king_position, pieces, en_passant_square):
    res = set()
    double_jump_row_index = 6 if color == 1 else 1
    row_index, col_index = pos
    opposite_color = get_opposite_color(color)
    possible_single_jump_final_square = (row_index - color, col_index)
    if is_empty(possible_single_jump_final_square, pieces):
        add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_single_jump_final_square, None), color, king_position, pieces)
        possible_double_jump_final_square = (row_index - color * 2, col_index)
        if is_empty(possible_double_jump_final_square, pieces) and row_index == double_jump_row_index:
            add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_double_jump_final_square, None), color, king_position, pieces)
    if col_index != 0:
        possible_left_capture_pos = (row_index - color, col_index - 1)
        if possible_left_capture_pos in pieces[opposite_color]:
            add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_left_capture_pos, possible_left_capture_pos), color, king_position, pieces)
        elif possible_left_capture_pos == en_passant_square:
            add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_left_capture_pos, (row_index, possible_left_capture_pos[1])), color, king_position, pieces)
    if col_index != 7:
        possible_right_capture_pos = (row_index - color, col_index + 1)
        if possible_right_capture_pos in pieces[opposite_color]:
            add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_right_capture_pos, possible_right_capture_pos), color, king_position, pieces)
        elif possible_right_capture_pos == en_passant_square:
            add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_right_capture_pos, (row_index, possible_right_capture_pos[1])), color, king_position, pieces)
    return res

def rook_legal_moves(pos, color, pieces, king_position):
    res = set()
    row_index, col_index = pos
    opposite_color = get_opposite_color(color)
    # Sliding north:
    cur_pos = [row_index - 1, col_index]
    while True:
        possible_addition = tuple(cur_pos)
        if possible_addition[0] == -1 or possible_addition in pieces[color]:
            break
        if possible_addition in pieces[opposite_color]:
            add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, possible_addition), color, king_position, pieces)
            break
        add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, None), color, king_position, pieces)
        cur_pos[0] -= 1
    # Sliding east:
    cur_pos = [row_index, col_index + 1]
    while True:
        possible_addition = tuple(cur_pos)
        if possible_addition[1] == 8 or possible_addition in pieces[color]:
            break
        if possible_addition in pieces[opposite_color]:
            add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, possible_addition), color, king_position, pieces)
            break
        add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, None), color, king_position, pieces)
        cur_pos[1] += 1
    # Sliding south:
    cur_pos = [row_index + 1, col_index]
    while True:
        possible_addition = tuple(cur_pos)
        if possible_addition[0] == 8 or possible_addition in pieces[color]:
            break
        if possible_addition in pieces[opposite_color]:
            add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, possible_addition), color, king_position, pieces)
            break
        add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, None), color, king_position, pieces)
        cur_pos[0] += 1
    # Sliding west:
    cur_pos = [row_index, col_index - 1]
    while True:
        possible_addition = tuple(cur_pos)
        if possible_addition[1] == -1 or possible_addition in pieces[color]:
            break
        if possible_addition in pieces[opposite_color]:
            add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, possible_addition), color, king_position, pieces)
            break
        add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, None), color, king_position, pieces)
        cur_pos[1] -= 1
    #
    return res

def knight_legal_moves(pos, color, king_position, pieces):
    res = set()
    row_index, col_index = pos
    opposite_color = get_opposite_color(color)
    not_on_top_edge = row_index != 0
    not_close_to_top_edge = not_on_top_edge and row_index != 1
    not_on_right_edge = col_index != 7
    not_close_to_right_edge = not_on_right_edge and col_index != 6
    not_on_bottom_edge = row_index != 7
    not_close_to_bottom_edge = not_on_bottom_edge and row_index != 6
    not_on_left_edge = col_index != 0
    not_close_to_left_edge = not_on_left_edge and col_index != 1
    # Big up
    if not_close_to_top_edge:
        # Small left
        if not_on_left_edge:
            helper(res, pos, (row_index - 2, col_index - 1), pieces, color, opposite_color, king_position)
        # Small right
        if not_on_right_edge:
            helper(res, pos, (row_index - 2, col_index + 1), pieces, color, opposite_color, king_position)
    # Big right
    if not_close_to_right_edge:
        # Small up
        if not_on_top_edge:
            helper(res, pos, (row_index - 1, col_index + 2), pieces, color, opposite_color, king_position)
        # Small down
        if not_on_bottom_edge:
            helper(res, pos, (row_index + 1, col_index + 2), pieces, color, opposite_color, king_position)
    # Big down
    if not_close_to_bottom_edge:
        # Small right
        if not_on_right_edge:
            helper(res, pos, (row_index + 2, col_index + 1), pieces, color, opposite_color, king_position)
        # Small left
        if not_on_left_edge:
            helper(res, pos, (row_index + 2, col_index - 1), pieces, color, opposite_color, king_position)
    # Big left
    if not_close_to_left_edge:
        # Small down
        if not_on_bottom_edge:
            helper(res, pos, (row_index + 1, col_index - 2), pieces, color, opposite_color, king_position)
        # Small up
        if not_on_top_edge:
            helper(res, pos, (row_index - 1, col_index - 2), pieces, color, opposite_color, king_position)
    #
    return res

def bishop_legal_moves(pos, color, pieces, king_position):
    res = set()
    row_index, col_index = pos
    opposite_color = get_opposite_color(color)
    # Sliding northeast:
    cur_pos = [row_index - 1, col_index + 1]
    while True:
        possible_addition = tuple(cur_pos)
        if possible_addition[0] == -1 or possible_addition[1] == 8 or possible_addition in pieces[color]:
            break
        if possible_addition in pieces[opposite_color]:
            add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, possible_addition), color, king_position, pieces)
            break
        add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, None), color, king_position, pieces)
        cur_pos[0] -= 1
        cur_pos[1] += 1
    # Sliding southeast:
    cur_pos = [row_index + 1, col_index + 1]
    while True:
        possible_addition = tuple(cur_pos)
        if possible_addition[0] == 8 or possible_addition[1] == 8 or possible_addition in pieces[color]:
            break
        if possible_addition in pieces[opposite_color]:
            add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, possible_addition), color, king_position, pieces)
            break
        add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, None), color, king_position, pieces)
        cur_pos[0] += 1
        cur_pos[1] += 1
    # Sliding southwest:
    cur_pos = [row_index + 1, col_index - 1]
    while True:
        possible_addition = tuple(cur_pos)
        if possible_addition[0] == 8 or possible_addition[1] == -1 or possible_addition in pieces[color]:
            break
        if possible_addition in pieces[opposite_color]:
            add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, possible_addition), color, king_position, pieces)
            break
        add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, None), color, king_position, pieces)
        cur_pos[0] += 1
        cur_pos[1] -= 1
    # Sliding northwest:
    cur_pos = [row_index - 1, col_index - 1]
    while True:
        possible_addition = tuple(cur_pos)
        if possible_addition[0] == -1 or possible_addition[1] == -1 or possible_addition in pieces[color]:
            break
        if possible_addition in pieces[opposite_color]:
            add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, possible_addition), color, king_position, pieces)
            break
        add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, None), color, king_position, pieces)
        cur_pos[0] -= 1
        cur_pos[1] -= 1
    #
    return res

def queen_legal_moves(pos, color, pieces, king_position):
    res = set()
    row_index, col_index = pos
    opposite_color = get_opposite_color(color)
    # Sliding north:
    cur_pos = [row_index - 1, col_index]
    while True:
        possible_addition = tuple(cur_pos)
        if possible_addition[0] == -1 or possible_addition in pieces[color]:
            break
        if possible_addition in pieces[opposite_color]:
            add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, possible_addition), color, king_position, pieces)
            break
        add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, None), color, king_position, pieces)
        cur_pos[0] -= 1
    # Sliding northeast:
    cur_pos = [row_index - 1, col_index + 1]
    while True:
        possible_addition = tuple(cur_pos)
        if possible_addition[0] == -1 or possible_addition[1] == 8 or possible_addition in pieces[color]:
            break
        if possible_addition in pieces[opposite_color]:
            add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, possible_addition), color, king_position, pieces)
            break
        add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, None), color, king_position, pieces)
        cur_pos[0] -= 1
        cur_pos[1] += 1
    # Sliding east:
    cur_pos = [row_index, col_index + 1]
    while True:
        possible_addition = tuple(cur_pos)
        if possible_addition[1] == 8 or possible_addition in pieces[color]:
            break
        if possible_addition in pieces[opposite_color]:
            add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, possible_addition), color, king_position, pieces)
            break
        add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, None), color, king_position, pieces)
        cur_pos[1] += 1
    # Sliding southeast:
    cur_pos = [row_index + 1, col_index + 1]
    while True:
        possible_addition = tuple(cur_pos)
        if possible_addition[0] == 8 or possible_addition[1] == 8 or possible_addition in pieces[color]:
            break
        if possible_addition in pieces[opposite_color]:
            add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, possible_addition), color, king_position, pieces)
            break
        add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, None), color, king_position, pieces)
        cur_pos[0] += 1
        cur_pos[1] += 1
    # Sliding south:
    cur_pos = [row_index + 1, col_index]
    while True:
        possible_addition = tuple(cur_pos)
        if possible_addition[0] == 8 or possible_addition in pieces[color]:
            break
        if possible_addition in pieces[opposite_color]:
            add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, possible_addition), color, king_position, pieces)
            break
        add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, None), color, king_position, pieces)
        cur_pos[0] += 1
    # Sliding southwest:
    cur_pos = [row_index + 1, col_index - 1]
    while True:
        possible_addition = tuple(cur_pos)
        if possible_addition[0] == 8 or possible_addition[1] == -1 or possible_addition in pieces[color]:
            break
        if possible_addition in pieces[opposite_color]:
            add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, possible_addition), color, king_position, pieces)
            break
        add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, None), color, king_position, pieces)
        cur_pos[0] += 1
        cur_pos[1] -= 1
    # Sliding west:
    cur_pos = [row_index, col_index - 1]
    while True:
        possible_addition = tuple(cur_pos)
        if possible_addition[1] == -1 or possible_addition in pieces[color]:
            break
        if possible_addition in pieces[opposite_color]:
            add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, possible_addition), color, king_position, pieces)
            break
        add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, None), color, king_position, pieces)
        cur_pos[1] -= 1
    # Sliding northwest:
    cur_pos = [row_index - 1, col_index - 1]
    while True:
        possible_addition = tuple(cur_pos)
        if possible_addition[0] == -1 or possible_addition[1] == -1 or possible_addition in pieces[color]:
            break
        if possible_addition in pieces[opposite_color]:
            add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, possible_addition), color, king_position, pieces)
            break
        add_move_to_res_if_doesnt_leave_king_in_check(res, (pos, possible_addition, None), color, king_position, pieces)
        cur_pos[0] -= 1
        cur_pos[1] -= 1
    #
    return res

def king_legal_moves(pos, color, pieces, castling_rights):
    res = set()
    row_index, col_index = pos
    not_on_top_edge = row_index != 0
    not_on_right_edge = col_index != 7
    not_on_bottom_edge = row_index != 7
    not_on_left_edge = col_index != 0
    opposite_color = get_opposite_color(color)
    squares_threatened_by_opponent = squares_threatened_by_color(opposite_color, pieces)
    # North:
    if not_on_top_edge:
        possible_addition = (row_index - 1, col_index)
        helper(res, pos, possible_addition, pieces, color, opposite_color, possible_addition)
        # Northeast:
        if not_on_right_edge:
            possible_addition = (row_index - 1, col_index + 1)
            helper(res, pos, possible_addition, pieces, color, opposite_color, possible_addition)
        # Northwest:
        if not_on_left_edge:
            possible_addition = (row_index - 1, col_index - 1)
            helper(res, pos, possible_addition, pieces, color, opposite_color, possible_addition)
    # South
    if not_on_bottom_edge:
        possible_addition = (row_index + 1, col_index)
        helper(res, pos, possible_addition, pieces, color, opposite_color, possible_addition)
        # Southeast:
        if not_on_right_edge:
            possible_addition = (row_index + 1, col_index + 1)
            helper(res, pos, possible_addition, pieces, color, opposite_color, possible_addition)
        # Southwest:
        if not_on_left_edge:
            possible_addition = (row_index + 1, col_index - 1)
            helper(res, pos, possible_addition, pieces, color, opposite_color, possible_addition)
    # East:
    if not_on_right_edge:
        possible_addition = (row_index, col_index + 1)
        helper(res, pos, possible_addition, pieces, color, opposite_color, possible_addition)
    # West:
    if not_on_left_edge:
        possible_addition = (row_index, col_index - 1)
        helper(res, pos, possible_addition, pieces, color, opposite_color, possible_addition)
    #
    if pos not in squares_threatened_by_opponent:
        if color == 1:
            kingside_castling_right = castling_rights[0]
            queenside_castling_right = castling_rights[1]
            castling_row_index = 7
        else:
            kingside_castling_right = castling_rights[2]
            queenside_castling_right = castling_rights[3]
            castling_row_index = 0
        if kingside_castling_right:
            square_1_to_right_of_king = (castling_row_index, 5)
            if is_empty(square_1_to_right_of_king, pieces) and square_1_to_right_of_king not in squares_threatened_by_opponent:
                square_2_to_right_of_king = (castling_row_index, 6)
                if is_empty(square_2_to_right_of_king, pieces) and square_2_to_right_of_king not in squares_threatened_by_opponent:
                    res.add((pos, square_2_to_right_of_king, None))
        if queenside_castling_right:
            square_1_to_left_of_king = (castling_row_index, 3)
            if is_empty(square_1_to_left_of_king, pieces) and square_1_to_left_of_king not in squares_threatened_by_opponent:
                square_2_to_left_of_king = (castling_row_index, 2)
                if is_empty(square_2_to_left_of_king, pieces) and square_2_to_left_of_king not in squares_threatened_by_opponent:
                    if is_empty((castling_row_index, 1), pieces):
                        res.add((pos, square_2_to_left_of_king, None))
    return res

def legal_moves(color, pieces, castling_rights, king_position, en_passant_square):
    res = set()
    for pos, piece in pieces[color].copy().items():
        piece_type = piece * color
        if piece_type == 1:
            res.update(pawn_legal_moves(pos, color, king_position, pieces, en_passant_square))
        elif piece_type == 2:
            res.update(rook_legal_moves(pos, color, pieces, king_position))
        elif piece_type == 3:
            res.update(knight_legal_moves(pos, color, king_position, pieces))
        elif piece_type == 4:
            res.update(bishop_legal_moves(pos, color, pieces, king_position))
        elif piece_type == 5:
            res.update(queen_legal_moves(pos, color, pieces, king_position))
        else:
            res.update(king_legal_moves(pos, color, pieces, castling_rights))
    return res

def execute_move(move, game_state):
    pos_i, pos_f, pos_captured_piece = move
    color = game_state['feature_vector'][ACTIVE_COLOR_FV_INDEX]
    if color == 1:
        opposite_color = -1
        queen = 5
        rook = 2
        king = 6
        promotion_row_index = 0
        castling_row_index = 7
        opponent_castling_row_index = 0
        kingside_castling_right_fv_index = WHITE_KINGSIDE_CASTLING_RIGHT_FV_INDEX
        queenside_castling_right_fv_index = WHITE_QUEENSIDE_CASTLING_RIGHT_FV_INDEX
        opponent_kingside_castling_right_fv_index = BLACK_KINGSIDE_CASTLING_RIGHT_FV_INDEX
        opponent_queenside_castling_right_fv_index = BLACK_QUEENSIDE_CASTLING_RIGHT_FV_INDEX
        pawn_double_jump_row_index_i = 6
        pawn_double_jump_row_index_f = 4
        new_en_passant_square_row_index = 5
    else:
        opposite_color = 1
        queen = -5
        rook = -2
        king = -6
        promotion_row_index = 7
        castling_row_index = 0
        opponent_castling_row_index = 7
        kingside_castling_right_fv_index = BLACK_KINGSIDE_CASTLING_RIGHT_FV_INDEX
        queenside_castling_right_fv_index = BLACK_QUEENSIDE_CASTLING_RIGHT_FV_INDEX
        opponent_kingside_castling_right_fv_index = WHITE_KINGSIDE_CASTLING_RIGHT_FV_INDEX
        opponent_queenside_castling_right_fv_index = WHITE_QUEENSIDE_CASTLING_RIGHT_FV_INDEX
        pawn_double_jump_row_index_i = 1
        pawn_double_jump_row_index_f = 3
        new_en_passant_square_row_index = 2
    
    # Changing halfmoves_since_last_pawn_move_or_capture: If the move is a capture or a pawn move, set to 0, otherwise increment by 1
    if pos_captured_piece or game_state['pieces'][color][pos_i] == color:
        game_state['halfmoves_since_last_pawn_move_or_capture'] = 0
        game_state['past_positions'] = defaultdict(int)
    else:
        if game_state['halfmoves_since_last_pawn_move_or_capture'] == 99:
            game_state['status'] = 'Draw by 50-move-rule'
            return
        game_state['halfmoves_since_last_pawn_move_or_capture'] += 1
    
    # Increment move number
    if color == -1:
        game_state['move_number'] += 1

    # Changing board state: special cases = [castling, pawn promotion, en passant], default = move the piece
    # Default:
    if pos_captured_piece:
        game_state['pieces'][opposite_color].pop(pos_captured_piece)
        game_state['feature_vector'][pos_captured_piece[0] * 8 + pos_captured_piece[1]] = 0
    game_state['pieces'][color][pos_f] = game_state['pieces'][color][pos_i]
    game_state['feature_vector'][pos_f[0] * 8 + pos_f[1]] = game_state['pieces'][color][pos_i]
    game_state['pieces'][color].pop(pos_i)
    game_state['feature_vector'][pos_i[0] * 8 + pos_i[1]] = 0
    if game_state['pieces'][color][pos_f] == king:
        game_state['king_positions'][color] = pos_f
    if game_state['pieces'][color][pos_f] == color and pos_f[0] == promotion_row_index:
        game_state['pieces'][color][pos_f] = queen
        game_state['feature_vector'][pos_f[0] * 8 + pos_f[1]] = queen

    # Castling:
    if move == ((castling_row_index, 4), (castling_row_index, 6), None) and game_state['feature_vector'][kingside_castling_right_fv_index]:
        game_state['pieces'][color].pop((castling_row_index, 7))
        game_state['feature_vector'][castling_row_index * 8 + 7] = 0
        game_state['pieces'][color][(castling_row_index, 5)] = rook
        game_state['feature_vector'][castling_row_index * 8 + 5] = rook
    elif move == ((castling_row_index, 4), (castling_row_index, 2), None) and game_state['feature_vector'][queenside_castling_right_fv_index]:
        game_state['pieces'][color].pop((castling_row_index, 0))
        game_state['feature_vector'][castling_row_index * 8] = 0
        game_state['pieces'][color][(castling_row_index, 3)] = rook
        game_state['feature_vector'][castling_row_index * 8 + 3] = rook

    # Changing castling rights: if you move your king or one of your rooks for the first time, or if you capture one of your opponents rooks
    if pos_i == (castling_row_index, 4):
        if game_state['feature_vector'][kingside_castling_right_fv_index]:
            game_state['feature_vector'][kingside_castling_right_fv_index] = 0
        if game_state['feature_vector'][queenside_castling_right_fv_index]:
            game_state['feature_vector'][queenside_castling_right_fv_index] = 0
    elif pos_i == (castling_row_index, 7) and game_state['feature_vector'][kingside_castling_right_fv_index]:
        game_state['feature_vector'][kingside_castling_right_fv_index] = 0
    elif pos_i == (castling_row_index, 0) and game_state['feature_vector'][queenside_castling_right_fv_index]:
        game_state['feature_vector'][queenside_castling_right_fv_index] = 0
    if pos_f == (opponent_castling_row_index, 0) and game_state['feature_vector'][opponent_queenside_castling_right_fv_index]:
        game_state['feature_vector'][opponent_queenside_castling_right_fv_index] = 0
    elif pos_f == (opponent_castling_row_index, 7) and game_state['feature_vector'][opponent_kingside_castling_right_fv_index]:
        game_state['feature_vector'][opponent_kingside_castling_right_fv_index] = 0
    
    # Changing en passant square: If your move is a pawn double-jump, set the en passant square accordingly, else set it to [-1, -1]
    if game_state['pieces'][color][pos_f] == color and pos_i[0] == pawn_double_jump_row_index_i and pos_f[0] == pawn_double_jump_row_index_f:
        game_state['feature_vector'][EN_PASSANT_SQUARE_ROW_INDEX_FV_INDEX], game_state['feature_vector'][EN_PASSANT_SQUARE_COLUMN_INDEX_FV_INDEX] = new_en_passant_square_row_index, pos_f[1]
    else:
        game_state['feature_vector'][EN_PASSANT_SQUARE_ROW_INDEX_FV_INDEX], game_state['feature_vector'][EN_PASSANT_SQUARE_COLUMN_INDEX_FV_INDEX] = -1, -1
    
    # Check for draw by threefold repetition:
    # "Two positions are by definition 'the same' if the same types of pieces occupy the same squares, the same player 
    # has the move, the remaining castling rights are the same and the possibility to capture en passant is the same."
    position = tuple(game_state['feature_vector'])
    if game_state['past_positions'][position] == 2:
        game_state['status'] = 'Draw by threefold repetition'
        return
    else:
        game_state['past_positions'][position] += 1

    # Check for draw by insufficient material:
    num_white_pieces = len(game_state['pieces'][1])
    num_black_pieces = len(game_state['pieces'][-1])
    num_pieces = num_white_pieces + num_black_pieces
    if num_white_pieces == 2 and 4 in game_state['pieces'][1].values() and num_black_pieces == 2 and -4 in game_state['pieces'][-1].values():
        for pos, piece in game_state['pieces'][1].items():
            if piece == 4:
                white_bishop_pos = pos
                break
        for pos, piece in game_state['pieces'][-1].items():
            if piece == -4:
                black_bishop_pos = pos
                break
        if (white_bishop_pos[0] + white_bishop_pos[1]) % 2 == (black_bishop_pos[0] + black_bishop_pos[1]) % 2:
            game_state['status'] = 'Draw by insufficient material (king and bishop versus king and bishop with the bishops on the same color)'
            return
    elif num_pieces == 3:
        if num_white_pieces == 2:
            white_pieces = game_state['pieces'][1].values()
            if 3 in white_pieces:
                game_state['status'] = 'Draw by insufficient material (king and knight versus king)'
                return
            if 4 in white_pieces:
                game_state['status'] = 'Draw by insufficient material (king and bishop versus king)'
                return
        else:
            black_pieces = game_state['pieces'][-1].values()
            if -3 in black_pieces:
                game_state['status'] = 'Draw by insufficient material (king and knight versus king)'
                return
            if -4 in black_pieces:
                game_state['status'] = 'Draw by insufficient material (king and bishop versus king)'
                return
    elif num_pieces == 2:
        game_state['status'] = 'Draw by insufficient material (king versus king)'
        return

    # Always change the active color to the opposite of what it currently is
    game_state['feature_vector'][ACTIVE_COLOR_FV_INDEX] = opposite_color

    game_state['FEN'] = get_FEN(game_state['feature_vector'], game_state['halfmoves_since_last_pawn_move_or_capture'], game_state['move_number'])

    game_state['legal_moves'] = legal_moves(opposite_color, game_state['pieces'], tuple(game_state['feature_vector'][WHITE_KINGSIDE_CASTLING_RIGHT_FV_INDEX : BLACK_QUEENSIDE_CASTLING_RIGHT_FV_INDEX + 1]), tuple(game_state['king_positions'][opposite_color]), tuple(game_state['feature_vector'][EN_PASSANT_SQUARE_ROW_INDEX_FV_INDEX : EN_PASSANT_SQUARE_COLUMN_INDEX_FV_INDEX + 1]))

    if not len(game_state['legal_moves']):
        if is_color_in_check(color, game_state['king_positions'][opposite_color], game_state['pieces']):
            if color == 1:
                game_state['status'] = 'White checkmates black'
            else:
                game_state['status'] = 'Black checkmates white'
        else:
            if color == 1:
                game_state['status'] = 'White stalemates black'
            else:
                game_state['status'] = 'Black stalemates white'
        return





##################################
# Debugging section
##################################

import random
from tqdm import tqdm
import time

symbols = {
    0: ' ', 1: '♙', 2: '♖', 3: '♘', 4: '♗', 5: '♕', 6: '♔',
    -1: '♟', -2: '♜', -3: '♞', -4: '♝', -5: '♛', -6: '♚'
}

def display_board(feature_vector):
    print(' --- --- --- --- --- --- --- --- ')
    for i in range(8):
        print('| ' + ' '.join(map(lambda x : symbols[x] + ' |', feature_vector[i * 8 : 8 * (i + 1)])))
        print(' --- --- --- --- --- --- --- --- ')
    print()


def test_game():
    game_state = get_fresh_game_state()
    while True:
        print(f'Move {game_state['move_number']} ({'white' if game_state['feature_vector'][ACTIVE_COLOR_FV_INDEX] == 1 else 'black'}):')
        execute_move(random.choice(tuple(game_state['legal_moves'])), game_state)
        print(game_state['FEN'])
        print(game_state['feature_vector'])
        display_board(game_state['feature_vector'])
        if game_state['status'] != 'live':
            print(game_state['status'])
            break
        # time.sleep(1)

def run_games(displaying=False):
    num_games = 1
    results = defaultdict(int)
    for i in tqdm(range(num_games)):
        game_state = get_fresh_game_state()
        while True:
            if displaying: print(f'Move {game_state['move_number']} ({'white' if game_state['feature_vector'][ACTIVE_COLOR_FV_INDEX] == 1 else 'black'}):')
            execute_move(random.choice(tuple(game_state['legal_moves'])), game_state)
            if displaying:
                print(f'FEN: {game_state['FEN']}')
                display_board(game_state['feature_vector'])
            if game_state['status'] != 'live' or game_state['move_number'] == 41:
                if displaying: print(game_state['status'])
                results[game_state['status']] += 1
                break
    for key, value in results.items():
        print(f'{key}: {value}')


# test_game()

# run_games(displaying=True)
