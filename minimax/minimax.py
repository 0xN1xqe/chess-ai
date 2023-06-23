# https://python-chess.readthedocs.io/en/latest/
# https://en.wikipedia.org/wiki/Algebraic_notation_(chess)
import chess


# Evaluation function to assign a score to a given chess position
def evaluate(board):
    # In this example, we simply count the material advantage for the side to move
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
        if piece is not None and piece.piece_type != 6:
            value = piece_values.get(piece.piece_type)
            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value

    return score


# Minimax function with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            max_eval = max(max_eval, minimax(board, depth - 1, alpha, beta, False))
            board.pop()
            alpha = max(alpha, max_eval)
            if alpha >= beta:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            min_eval = min(min_eval, minimax(board, depth - 1, alpha, beta, True))
            board.pop()
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        return min_eval


# Main function to initiate the minimax search
def find_best_move(board, depth):
    best_eval = float('-inf')
    best_move = None
    alpha = float('-inf')
    beta = float('inf')
    for move in board.legal_moves:
        board.push(move)
        move_eval = minimax(board, depth - 1, alpha, beta, False)
        board.pop()
        if move_eval > best_eval:
            best_eval = move_eval
            best_move = move
    return best_move


# Example usage
board = chess.Board()
best_move = find_best_move(board, depth=3)
print("Best move:", best_move)
