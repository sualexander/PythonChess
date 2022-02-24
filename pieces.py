#checks valid moves for each type of piece
from globals import *

#gets list of valid moves
def valid(piece_name, piece_index):
    if piece_name != "none":
        return remove_negative(globals()[piece_name](piece_index))
    else:
        print("invalid selection")
        return

def get_diagonals(piece_index):
    valid_moves = []
    row = piece_index[0]
    col = piece_index[1]
    #upper left
    for i in range(7):
        if board[row - i - 1][col - i - 1] == 0:
            valid_moves.append([row - i - 1, col - i - 1])
        elif board[row - i - 1][col - i - 1] * board[row][col] < 0:
            valid_moves.append([row - i - 1, col - i - 1])
            break
        else:
            break
    #lower left
    for i in range(7):
        if board[row + i + 1][col - i - 1] == 0:
            valid_moves.append([row + i + 1, col - i - 1])
        elif board[row + i + 1][col - i - 1] * board[row][col] < 0:
            valid_moves.append([row + i + 1, col - i - 1])
            break
        else:
            break
    #lower right
    for i in range(7):
        if board[row + i + 1][col + i + 1] == 0:
            valid_moves.append([row + i + 1, col + i + 1])
        elif board[row + i + 1][col + i + 1] * board[row][col] < 0:
            valid_moves.append([row + i + 1, col + i + 1])
            break
        else:
            break
    #upper right
    for i in range(7):
        if board[row - i - 1][col + i + 1] == 0:
            valid_moves.append([row - i - 1, col + i + 1])
        elif board[row - i - 1][col + i + 1] * board[row][col] < 0:
            valid_moves.append([row - i - 1, col + i + 1])
            break
        else:
            break
    return valid_moves

def get_colrows(piece_index):
    valid_moves = []
    row = piece_index[0]
    col = piece_index[1]
    n = -1
    for k in range(2):
        #columns
        for i in range(7):
            if board[row][col + (i + 1)*n] == 0:
                valid_moves.append([row, col + (i + 1)*n])
            elif board[row][col + (i + 1)*n] * board[row][col] < 0:
                valid_moves.append([row, col + (i + 1)*n])
                break
            else:
                break
        #rows
        for i in range(7):
            if board[row + (i + 1)*n][col] == 0:
                valid_moves.append([row + (i + 1)*n, col])
            elif board[row + (i + 1)*n][col] * board[row][col] < 0:
                valid_moves.append([row + (i + 1)*n, col])
                break
            else:
                break
        n = 1
    return valid_moves

def rook(piece_index):
    return get_colrows(piece_index)

def bishop(piece_index):
    return get_diagonals(piece_index)

def queen(piece_index):
    return get_colrows(piece_index) + get_diagonals(piece_index)

def king(piece_index):
    valid_moves = []
    row = piece_index[0]
    col = piece_index[1]
    for i in range(3):
        for j in range(3):
            if (board[row - 1 + i][col - 1 + j] == 0) or \
                    (board[row - 1 + i][col - 1 + j] * board[row][col] < 0):
                valid_moves.append([row - 1 + i,col - 1 + j])
    return valid_moves

def castle(piece_index):
    valid_moves = []
    if board[piece_index[0]][piece_index[1]] > 0:
        xcan_castle = wcan_castle
    else:
        xcan_castle = bcan_castle
    if xcan_castle[0] == 1:
        #queenside
        n = -1
        s = 1
        if any_castle(piece_index,n,s):
            valid_moves.append([piece_index[0], piece_index[1] - 2])
    if xcan_castle[1] == 1:
        #kingside
        n = 1
        s = 2
        if any_castle(piece_index,n,s):
            valid_moves.append([piece_index[0], piece_index[1] + 2])
    return valid_moves

def any_castle(piece_index,n,s):
    squares = []
    #no pieces in between rook and king
    for i in range(piece_index[1]-s):
        if board[piece_index[0]][piece_index[1]+(i+1)*n] != 0:
            empty = False
            return empty
        squares.append([piece_index[0],piece_index[1]+(i+1)*n])
    #squares between rook and king inclusive cannot be in check or will be in check
    squares.append([piece_index[0],piece_index[1]+(piece_index[1]-s+1)*n])
    squares.append([piece_index[0],piece_index[1]])
    if check_check(squares,piece_index) != squares:
        return False
    else:
        return True

def knight(piece_index):
    valid_moves = []
    row = piece_index[0]
    col = piece_index[1]
    for i in range(5):
        for j in range(5):
            if (abs(-2 + i) ** 2) + (abs(-2 + j)) ** 2 == 5:
                if (board[row - 2 + i][col - 2 + j] == 0) or \
                        board[row - 2 + i][col - 2 + j] * board[row][col] < 0:
                    valid_moves.append([row - 2 + i,col - 2 + j])
    return valid_moves

def pawn(piece_index):
    valid_moves = []
    row = piece_index[0]
    col = piece_index[1]
    if board[row][col] < 0:
        n = -1
        row_start = 1
    else:
        n = 1
        row_start = 6
    if (board[row-1*n][col] == 0):
        valid_moves.append([row-1*n,col])
    if board[row-1*n][col-1] * board[row][col] < 0:
        valid_moves.append([row-1*n,col-1])
    if board[row-1*n][col+1] * board[row][col] < 0:
        valid_moves.append([row-1*n,col+1])
    #double from starting row
    if (row == row_start) and (board[row-2*n][col] == 0):
        valid_moves.append([row-2*n,col])
    return valid_moves

def pawn_promotion(piece_index):
    not_valid = True
    while not_valid:
        promote = input("promote?")
        if (promote == "y") or (promote == "yes"):
            not_valid = False
            piece = input("queen, rook, bishop, knight")
            names = {'rook': 1, 'knight': 2, 'bishop': 3, 'queen': 4}
            if board[piece_index[0]][piece_index[1]] > 0:
                abrv = names.get(piece, "none")
            else:
                abrv = -names.get(piece, "none")
            if abrv == "none":
                print("invalid selection")
                not_valid = True
        elif (promote == "n") or (promote == "no"):
            not_valid = False
            if board[piece_index[0]][piece_index[1]] > 0:
                abrv = board[piece_index[0]][piece_index[1]]
            else:
                abrv = board[piece_index[0]][piece_index[1]]
            if abrv == "none":
                print("invalid selection")
                not_valid = True
        else:
            print("invalid selection")
            not_valid = True
    return abrv

def en_passant(piece_index):
    valid_moves = []
    if past_move[0][0] == 1:
        n = 1
    else:
        n = -1
    if [piece_index[0],piece_index[1] - 1] == past_move[1]:
        valid_moves.append([past_move[1][0] -1*n,past_move[1][1]])
    if [piece_index[0],piece_index[1] + 1] == past_move[1]:
        valid_moves.append([past_move[1][0] -1*n,past_move[1][1]])
    return valid_moves

#modifies valid_moves so that a move cannot lead to check
def check_check(valid_moves,piece_index):
    index = []
    for i in range(8):
        for j in range(8):
            if board[i][j] * board[piece_index[0]][piece_index[1]] < 0:
                index.append([i, j])
            elif abs(board[i][j]) == 5:
                king = [i, j]
    temp_moves = valid_moves.copy()
    temp_index = king
    for x in valid_moves:
        if piece_index == temp_index:
            king = x
        temp = board[x[0]][x[1]]
        board[x[0]][x[1]] = board[piece_index[0]][piece_index[1]]
        board[piece_index[0]][piece_index[1]] = 0

        for i in index:
            valid_squares = valid(piece_lookup(i), i)
            if king in valid_squares:
                temp_moves.remove(x)
                break
        board[piece_index[0]][piece_index[1]] = board[x[0]][x[1]]
        board[x[0]][x[1]] = temp

    valid_moves = temp_moves
    valid_moves = remove_negative(valid_moves)
    return valid_moves

#converts move index to piece name at target square
def piece_lookup(piece_index):
    for i in range(8):
        for j in range(8):
            if [i,j] == piece_index:
                piece_abrv = board[i][j]
                names = {6: 'pawn', 1: 'rook', 2: 'knight', 3: 'bishop', 4: 'queen', 5: 'king'}
                piece_name = names.get(abs(piece_abrv), "none")
                return piece_name
    return "none"

def remove_negative(valid_moves):
    temp_moves = valid_moves.copy()
    for i in valid_moves:
        if i[0] < 0 or i[1] < 0:
            temp_moves.remove(i)
        elif i[0] > 7 or i[1] > 7:
            temp_moves.remove(i)
    valid_moves = temp_moves
    return valid_moves