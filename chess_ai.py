
import random
import chess_ai_piece_scores as ps

PIECE_TYPE_SCORE = {'K': 0, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'P': 1}

MAX_VALUE = 10000
MIN_VALUE = -MAX_VALUE
DEPTH = 2

score = 0

def get_AI_move(gs, valid_moves, int_flag):

    # the way which the opponent's move is not considered.
    if int_flag == 0:
        random.shuffle(valid_moves)
        if gs.white_to_move:
            max_score = MIN_VALUE
            for move in valid_moves:
                gs.make_move(move[0], move[1])
                score = get_board_score(gs)
                if score > max_score:
                    max_score = score
                    next_move = move
                gs.undo_move()
        else:
            min_score = MAX_VALUE
            for move in valid_moves:
                gs.make_move(move[0], move[1])
                score = get_board_score(gs)
                if score < min_score:
                    min_score = score
                    next_move = move
                gs.undo_move()
            # print('chess_ai', min_score, next_move)
        return next_move

    # minimax
    elif int_flag == 1:
        random.shuffle(valid_moves)
        score, next_move = get_MiniMax_move(gs, valid_moves, DEPTH, gs.white_to_move)
        return next_move

    # negamax
    elif int_flag == 2:
        random.shuffle(valid_moves)
        if gs.white_to_move:
            turn_sign = 1
        else:
            turn_sign = -1
        score, next_move = get_NegaMax_move(gs, valid_moves, DEPTH, turn_sign)
        return next_move

    # negamax with aplha-beta
    elif int_flag == 3:
        random.shuffle(valid_moves)
        if gs.white_to_move:
            turn_sign = 1
        else:
            turn_sign = -1
        score, next_move = get_NegaMax_AlphaBeta_move(gs, valid_moves, DEPTH, turn_sign, MIN_VALUE, MAX_VALUE)
        return next_move


def get_board_score(gs):

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            score_piece_position = 0
            # print('get_board_score: ', square)
            if square[1] == 'N':
                score_piece_position = ps.Score_N[row][col]
            elif square[1] == 'B':
                score_piece_position = ps.Score_B[row][col]
            elif square[1] == 'Q':
                score_piece_position = ps.Score_Q[row][col]
            elif square[1] == 'K':
                score_piece_position = ps.Score_K[row][col]
            elif square[1] == 'R':
                if square[0] == 'w':
                    score_piece_position = ps.Score_wR[row][col]
                else:
                    score_piece_position = ps.Score_bR[row][col]
            else:
                if square[0] == 'w':
                    score_piece_position = ps.Score_wP[row][col]
                else:
                    score_piece_position = ps.Score_bP[row][col]

            # print('score_piece_position', score_piece_position)
            if square[0] == 'w':
                score += PIECE_TYPE_SCORE[square[1]] * 10
                # print('PIECE_TYPE_SCORE[square[1]] * 10', PIECE_TYPE_SCORE[square[1]] * 10)
                score += int(score_piece_position)
                # print('score_piece_position',score_piece_position)
            elif square[0] == 'b':
                score -= PIECE_TYPE_SCORE[square[1]] * 10
                # print('PIECE_TYPE_SCORE[square[1]] * 10', PIECE_TYPE_SCORE[square[1]] * 10)
                score -= int(score_piece_position)
                # print('score_piece_position',score_piece_position)

    return score

def get_MiniMax_move(gs, valid_moves, depth, white_and_black):

    next_move = ''
    if depth == 0:
        return get_board_score(gs)

    if len(valid_moves) == 0:
        if gs.checkMate:
            if gs.white_to_move:
                return MIN_VALUE  # 黒の勝ち
            else:
                return MAX_VALUE  # 白の勝ち
        else: #ステイルメイト or ドロー
            return 0

    if white_and_black:
        max_score = MIN_VALUE
        for move in valid_moves:
            gs.make_move(move[0], move[1])
            # depth-1＝0の場合、次の候補手は不要
            if depth > 1:
                next_moves = gs.get_valid_moves()
            else:
                next_moves = []
            score = get_MiniMax_move(gs, next_moves, depth -1, False)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        if depth == DEPTH:
            # print('max_score at depth==DEPTH = ', max_score, 'depth=', depth)
            return max_score, next_move
        else:
            # print('max_score at line 118= ', max_score, 'depth= ',depth)
            return max_score
    else:
        min_score = MAX_VALUE
        for move in valid_moves:
            gs.make_move(move[0], move[1])
            # deptsh-1＝0の場合、次の候補手は不要
            if depth > 1:
                next_moves = gs.get_valid_moves()
            else:
                next_moves = []
            # print('virtual move for AI: ', move)
            score = get_MiniMax_move(gs, next_moves, depth -1, True)
            if score < min_score:
                min_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()

        if depth == DEPTH:
            # print('min_score at depth==DEPTH = ', min_score, 'depth=', depth)
            return min_score, next_move
        else:
            # print('min_score at line 139', min_score, depth)
            return min_score


def get_NegaMax_move(gs, valid_moves, depth, turn_sign):
    # print('-----------------')
    # print('depth=',depth,'sign=',turn_sign)
    next_move = ''
    if depth == 0:
        return get_board_score(gs) * turn_sign

    if len(valid_moves) == 0:
        if gs.checkMate:
            if gs.white_to_move:
                return MIN_VALUE  # 黒の勝ち
            else:
                return MAX_VALUE  # 白の勝ち
        else: #ステイルメイト or ドロー
            return 0

    max_score = MIN_VALUE
    for move in valid_moves:
        gs.make_move(move[0], move[1])
        # depth-1＝0の場合、次の候補手は不要
        if depth > 1:
            next_moves = gs.get_valid_moves()
        else:
            next_moves = []
        score = -get_NegaMax_move(gs, next_moves, depth -1, -turn_sign)
        if score > max_score:
            max_score = score
            max_move = move
            if depth == DEPTH:
                next_move = move
        gs.undo_move()
    if depth == DEPTH:
        # print('final value ', max_score)
        return max_score, next_move
    else:
        # print('max_score, depth = ', max_score, depth)
        return max_score

def get_NegaMax_AlphaBeta_move(gs, valid_moves, depth, turn_sign, alpha, beta):

    next_move = ''

    if depth == 0:
        return get_board_score(gs) * turn_sign

    if len(valid_moves) == 0:
        if gs.checkMate:
            if gs.white_to_move:
                return MIN_VALUE  # 黒の勝ち
            else:
                return MAX_VALUE  # 白の勝ち
        else: #ステイルメイト or ドロー
            return 0

    max_score = MIN_VALUE
    # print('depth, len(valid_moves) = ', depth, len(valid_moves))
    count = 0
    for move in valid_moves:
        count += 1
        gs.make_move(move[0], move[1])
        if depth > 1:
            next_moves = gs.get_valid_moves()
        else:
            next_moves = []
        score = -get_NegaMax_AlphaBeta_move(gs, next_moves, depth-1, -turn_sign, -beta, -alpha)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        gs.undo_move()

        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            # print('count=', count)
            break

    if depth == DEPTH:
        return max_score, next_move
    else:
        return max_score


def get_board_score_piece_count(gs):

    # score_white = 0
    # score_black = 0
    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square[0] == 'w':
                # score_white += 1
                score += 1
            elif square[0] == 'b':
                # score_black += 1
                score -= 1

    # return score_white, score_black
    return score
