# https://python-chess.readthedocs.io/en/latest/
# https://en.wikipedia.org/wiki/Algebraic_notation_(chess)
import positions as p

import chess
import time


# Evaluation function to assign a score to a given chess position
def evaluate_values(board, is_white):
    score = 0
    piece_values = {
        chess.PAWN: 1,
        chess.BISHOP: 3,
        chess.KNIGHT: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9
    }

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        # ignore all pieces that are none or king
        if piece is not None and piece.piece_type != 6:
            value = piece_values.get(piece.piece_type)
            if is_white:
                if piece.color == chess.WHITE:
                    score += value
                else:
                    score -= value
            else:
                if piece.color == chess.BLACK:
                    score += value
                else:
                    score -= value

    return score


def pieces_of_my_color(board, is_white):
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        # ignore all pieces that are none or king
        if piece is not None and piece.piece_type != 6:
            if is_white:
                if piece.color == chess.WHITE:
                    score += 1
            else:
                if piece.color == chess.BLACK:
                    score += 1
    return score


def evaluate_positions(board, is_white):
    score = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        number_to_pieces = {
            1: p.Pawn,
            2: p.Knight,
            3: p.Bishop,
            4: p.Rook,
            5: p.Queen,
            6: p.KingEarly if pieces_of_my_color(board, is_white) > 16*0.60 else p.KingLate,
        }

        if piece is not None:
            positions = number_to_pieces.get(piece.piece_type)
            if is_white:
                if piece.color == chess.WHITE:
                    score += positions[square]
                else:
                    score -= positions[square]
            else:
                if piece.color == chess.BLACK:
                    score += positions.reverse()[square]
                else:
                    score -= positions.reverse()[square]

    return score


def evaluate_values_and_positions(board, is_white, values_param, positions_param):
    values_score = 0
    positions_score = 0

    piece_values = {
        chess.PAWN: 1,
        chess.BISHOP: 3,
        chess.KNIGHT: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9
    }

    number_to_pieces = {
        1: p.Pawn,
        2: p.Knight,
        3: p.Bishop,
        4: p.Rook,
        5: p.Queen,
        6: p.KingEarly if len(board.move_stack) < 20 else p.KingLate,
    }

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        # ignore all pieces that are none or king
        if piece is not None:
            value = piece_values.get(piece.piece_type)
            positions = number_to_pieces.get(piece.piece_type)
            if is_white:
                if piece.color == chess.WHITE:
                    positions_score += positions[square]
                    if piece.piece_type != 6:
                        values_score += value
                else:
                    positions_score -= positions[square]
                    if piece.piece_type != 6:
                        values_score -= value
            else:
                if piece.color == chess.BLACK:
                    positions_score += positions[square]
                    if piece.piece_type != 6:
                        values_score += value
                else:
                    positions_score -= positions[square]
                    if piece.piece_type != 6:
                        values_score -= value

    return positions_param * positions_score + values_param * values_score


# Minimax function with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizing_player, is_white, values_param, position_param):
    if depth == 0 or board.is_game_over():
        # return values_param * evaluate_values(board, is_white) + position_param * evaluate_positions(board, is_white)
        return evaluate_values_and_positions(board, is_white, values_param, position_param)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            max_eval = max(max_eval, minimax(board, depth - 1, alpha, beta, False, is_white, values_param, position_param))
            board.pop()
            alpha = max(alpha, max_eval)
            if alpha >= beta:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            min_eval = min(min_eval, minimax(board, depth - 1, alpha, beta, True, is_white, values_param, position_param))
            board.pop()
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        return min_eval


# Main function to initiate the minimax search
def find_best_move(board, depth, is_white, values_param, position_param):
    best_eval = float('-inf')
    best_move = None
    alpha = float('-inf')
    beta = float('inf')
    for move in board.legal_moves:
        board.push(move)
        move_eval = minimax(board, depth - 1, alpha, beta, False, is_white, values_param, position_param)
        board.pop()
        if move_eval > best_eval:
            best_eval = move_eval
            best_move = move
    return best_move


if __name__ == "__main__":

    start_time = time.time()

    # depth 3: 0.086698 s
    # depth 4: 1.0492200 s
    # depth 5: 4.04507160 s
    # depth 6: 58.5809996 s
    # depth 7: 268.734338 s

    # Best move: g1f3
    # 4.747699 seconds

    # Best move: g1h3
    # 3.660270 seconds

    # Best move: g1f3
    # 5.343630 seconds

    # Example usage
    board = chess.Board()
    best_move = find_best_move(board, 4, True, 1, 1)
    print("Best move:", best_move)

    print(f"{time.time() - start_time:.6f} seconds")
