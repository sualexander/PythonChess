from chess import *

def update_game(white_move):
    not_valid_move = True
    while not_valid_move:
        not_valid_move = update_move(white_move)

# asks user for move and evaluates validity of move
def update_move(white_move):
    print_board(white_move)
    piece = input("which piece?")  # eg: e4

    piece_index = num_to_index(piece)
    if (real_board.chess_board[piece_index[0]][piece_index[1]] < 0) == white_move:
        print("wrong color")
        return True
    piece_name = piece_lookup(real_board,piece_index)
    # returns array of allowed moves based on type of selected piece
    valid_moves = valid(real_board,piece_name, piece_index)
    if not valid_moves:
        print("no valid moves")
        return True
    # en passant
    en_passant_squares = []
    if piece_name == "pawn":
        en_passant_squares = en_passant(real_board,piece_index)
        valid_moves += en_passant_squares
    # checks if move would allow discovered check
    valid_moves = check_check(real_board,valid_moves, piece_index)
    # adds castling moves to valid_moves if allowed
    castle_squares = []
    if piece_name == "king":
        castle_squares = castle(real_board,piece_index)
        valid_moves += castle_squares
    if not valid_moves:
        print("no valid moves")
        return True

    move = input("enter your move")

    move_index = num_to_index(move)
    if compare(valid_moves, move_index):
        # pawn promotion
        if (piece_name == "pawn") and ((move_index[0] == 0) or (move_index[0] == 7)):
            promotion = True
        else:
            promotion = False
        # en passant
        if move_index in en_passant_squares:
            real_board.chess_board[real_board.past_move[1][0]][real_board.past_move[1][1]] = 0
        # castling
        elif move_index in castle_squares:
            move_rook(real_board,move_index)

        update_board(real_board,piece_index, move_index, promotion)
        if deliver_check(real_board,move_index):
            if check_mate(real_board,move_index):
                # check for draw
                if check_mate(real_board,move_index * -1):
                    print("STALEMATE!")
                    exit()
                else:
                    print("CHECKMATE!")
                    exit()
            else:
                print("CHECK!")
    else:
        print("invalid move")
        return True
