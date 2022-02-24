from chess import *
import random

def update_move(board,black_move):
    white_move = False
    pieces = []
    moves = []
    for i in range(8):
        for j in range(8):
            if board[i][j] < 0:
                pieces.append([i, j])

    while 1 > 0:
        i = random.choice(pieces)
        piece_index = i
        if (board[piece_index[0]][piece_index[1]] < 0) == white_move:
            continue
        piece_name = piece_lookup(piece_index)
        # returns array of allowed moves based on type of selected piece
        valid_moves = valid(piece_name, piece_index)
        if not valid_moves:
            continue
        # en passant
        #en_passant_squares = []
        if piece_name == "pawn":
            en_passant_squares = en_passant(piece_index)
            valid_moves += en_passant_squares
        # checks if move would allow discovered check
        valid_moves = check_check(valid_moves, piece_index)
        # adds castling moves to valid_moves if allowed
        #castle_squares = []
        if piece_name == "king":
            castle_squares = castle(piece_index)
            valid_moves += castle_squares
        #moves.append(valid_moves)
        update_board(i,random.choice(valid_moves),False)
        return not black_move