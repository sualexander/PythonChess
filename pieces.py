from globals import *

def get_diagonals(board,piece_index):
    valid_moves = []
    row = piece_index[0]
    col = piece_index[1]
    #upper left
    for i in range(7):
        if board.chess_board[row - i - 1][col - i - 1] == 0:
            valid_moves.append([row - i - 1, col - i - 1])
        elif board.chess_board[row - i - 1][col - i - 1] * board.chess_board[row][col] < 0:
            valid_moves.append([row - i - 1, col - i - 1])
            break
        else:
            break
    #lower left
    for i in range(7):
        if board.chess_board[row + i + 1][col - i - 1] == 0:
            valid_moves.append([row + i + 1, col - i - 1])
        elif board.chess_board[row + i + 1][col - i - 1] * board.chess_board[row][col] < 0:
            valid_moves.append([row + i + 1, col - i - 1])
            break
        else:
            break
    #lower right
    for i in range(7):
        if board.chess_board[row + i + 1][col + i + 1] == 0:
            valid_moves.append([row + i + 1, col + i + 1])
        elif board.chess_board[row + i + 1][col + i + 1] * board.chess_board[row][col] < 0:
            valid_moves.append([row + i + 1, col + i + 1])
            break
        else:
            break
    #upper right
    for i in range(7):
        if board.chess_board[row - i - 1][col + i + 1] == 0:
            valid_moves.append([row - i - 1, col + i + 1])
        elif board.chess_board[row - i - 1][col + i + 1] * board.chess_board[row][col] < 0:
            valid_moves.append([row - i - 1, col + i + 1])
            break
        else:
            break
    return valid_moves

def get_colrows(board,piece_index):
    valid_moves = []
    row = piece_index[0]
    col = piece_index[1]
    n = -1
    for k in range(2):
        #columns
        for i in range(7):
            if board.chess_board[row][col + (i + 1)*n] == 0:
                valid_moves.append([row, col + (i + 1)*n])
            elif board.chess_board[row][col + (i + 1)*n] * board.chess_board[row][col] < 0:
                valid_moves.append([row, col + (i + 1)*n])
                break
            else:
                break
        #rows
        for i in range(7):
            if board.chess_board[row + (i + 1)*n][col] == 0:
                valid_moves.append([row + (i + 1)*n, col])
            elif board.chess_board[row + (i + 1)*n][col] * board.chess_board[row][col] < 0:
                valid_moves.append([row + (i + 1)*n, col])
                break
            else:
                break
        n = 1
    return valid_moves
#####################################################

def rook(board,piece_index):
    return get_colrows(board,piece_index)

def bishop(board,piece_index):
    return get_diagonals(board,piece_index)

def queen(board,piece_index):
    return get_colrows(board,piece_index) + get_diagonals(board,piece_index)

def king(board,piece_index):
    valid_moves = []
    row = piece_index[0]
    col = piece_index[1]
    for i in range(3):
        for j in range(3):
            if (board.chess_board[row - 1 + i][col - 1 + j] == 0) or \
                    (board.chess_board[row - 1 + i][col - 1 + j] * board.chess_board[row][col] < 0):
                valid_moves.append([row - 1 + i,col - 1 + j])
    return valid_moves

def knight(board,piece_index):
    valid_moves = []
    row = piece_index[0]
    col = piece_index[1]
    for i in range(5):
        for j in range(5):
            if (abs(-2 + i) ** 2) + (abs(-2 + j)) ** 2 == 5:
                if (board.chess_board[row - 2 + i][col - 2 + j] == 0) or \
                        board.chess_board[row - 2 + i][col - 2 + j] * board.chess_board[row][col] < 0:
                    valid_moves.append([row - 2 + i,col - 2 + j])
    return valid_moves

def pawn(board,piece_index):
    valid_moves = []
    row = piece_index[0]
    col = piece_index[1]
    if board.chess_board[row][col] < 0:
        n = -1
        row_start = 1
    else:
        n = 1
        row_start = 6
    if (board.chess_board[row-1*n][col] == 0):
        valid_moves.append([row-1*n,col])
    if board.chess_board[row-1*n][col-1] * board.chess_board[row][col] < 0:
        valid_moves.append([row-1*n,col-1])
    if board.chess_board[row-1*n][col+1] * board.chess_board[row][col] < 0:
        valid_moves.append([row-1*n,col+1])
    #double from starting row
    if (row == row_start) and (board.chess_board[row-2*n][col] == 0):
        valid_moves.append([row-2*n,col])
    return valid_moves



