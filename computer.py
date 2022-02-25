import dataclasses
import math
import random

from chess import *

def update_game(white_move):
    move = minimax(real_board, True, 3, white_move)[1]
    update_board(real_board,move[0], move[1], False)

def get_valid_moves(board,white_move):
    moves = []
    pieces = get_pieces(board,white_move)

    for i in pieces:
        piece_index = i
        piece_name = piece_lookup(board,piece_index)
        valid_moves = valid(board,piece_name,piece_index)  # returns array of allowed moves based on type of selected piece
        if not valid_moves:
            continue

        if piece_name == "pawn":  # en passant
            en_passant_squares = en_passant(board,piece_index)
            valid_moves += en_passant_squares
        valid_moves = check_check(board,valid_moves, piece_index) # checks if move would allow discovered check

        if piece_name == "king":  # adds castling moves to valid_moves if allowed
            castle_squares = castle(board,piece_index)
            valid_moves += castle_squares
        for n in valid_moves:
            moves.append([i,n])
    return moves

def minimax(board, maximizer, depth, white_move):
    if depth == 0:
        return evaluate(board, white_move), None
    moves = get_valid_moves(board,white_move)
    best_move = random.choice(moves)
    if maximizer:
        max_value = -math.inf
        for i in moves:
            unmake = update_board(board, i[0], i[1], False)
            value = minimax(board, False, depth-1, not white_move)[0]
            unupdate_board(board,i[0],i[1],unmake[0],unmake[1])
            if value > max_value:
                max_value = value
                best_move = i
        return max_value, best_move
    else:
        min_value = math.inf
        for i in moves:
            update_board(board, i[0], i[1], False)
            value = minimax(board, False, depth-1, not white_move)[0]
            if value < min_value:
                min_value = value
                best_move = i
        return min_value, best_move

def get_pieces(board,white_move):
    pieces = []
    if white_move:
        for i in range(8):
            for j in range(8):
                if board.chess_board[i][j] > 0:
                    pieces.append([i, j])
    else:
        for i in range(8):
            for j in range(8):
                if board.chess_board[i][j] < 0:
                    pieces.append([i, j])
    return pieces

def evaluate(board, white_move):
    piece_values = {1: 5, 2: 3, 3: 3, 4: 8, 5: 69}
    w_pieces = get_pieces(board,True)
    b_pieces = get_pieces(board,False)
    white = 0
    black = 0
    for i in w_pieces:
        white += piece_values.get(abs(board.chess_board[i[0]][i[1]]),0)
    for i in b_pieces:
        black += piece_values.get(abs(board.chess_board[i[0]][i[1]]),0)
    if white_move:
        return white-black
    else:
        return black-white
