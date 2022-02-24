from pieces import *

#draws board
def print_board():
    #if white move something
    print("white to move")
    print("black to move")
    num_to_display ={1: "W\u265C",2: "W\u265E",3: "W\u265D",4: "W\u265B",5: "W\u265A",6: "W\u265F",-1: "B\u265C",-2: "B\u265E",-3: "B\u265D",-4: "B\u265B",-5: "B\u265A",-6: "B\u265F"}
    for i in range(8):
        row_pic = []
        for j in range(8):
            pic = num_to_display.get(board[i][j], "--")
            row_pic.append(pic)
        print(row_pic)

#updates board
def update_board(piece_index,move_index,promotion):
    global wcan_castle, bcan_castle, past_move
    #pawn promotion
    if promotion:
        abrv = pawn_promotion(piece_index)
    else:
        abrv = board[piece_index[0]][piece_index[1]]
    #en passant
    past_move = [piece_index,move_index]
    #checks if user has moved rooks or king or if rooks has been captured for castling
    if board[piece_index[0]][piece_index[1]] > 0:
        if abrv == 5:
            wcan_castle = [0,0]
        elif (abrv == 1 and piece_index[1] == 0) or (board[7][0] != 1):
            wcan_castle[0] = 0
        elif (abrv == 1 and piece_index[1] == 7) or (board[7][7] != 1):
            wcan_castle[1] = 0
    else:
        if abrv == -5:
            bcan_castle = [0,0]
        elif (abrv == -1 and piece_index[1] == 0) or (board[0][0] != -1):
            bcan_castle[0] = 0
        elif (abrv == -1 and piece_index[1] == 7) or (board[0][7] != -1):
            bcan_castle[1] = 0
    #modifies board with player move
    board[move_index[0]][move_index[1]] = abrv
    board[piece_index[0]][piece_index[1]] = 0

def deliver_check(move_index):
    index = []
    for i in range(8):
        for j in range(8):
            if board[i][j] * board[move_index[0]][move_index[1]] > 0:
                index.append([i, j])
            elif abs(board[i][j]) == 5:
                king = [i, j]
    for i in index:
        valid_squares = valid(piece_lookup(i),i)
        if king in valid_squares:
            return True
    return False

def check_mate(move_index):
    index = []
    escape_moves = []
    for i in range(8):
        for j in range(8):
            if board[i][j] * board[move_index[0]][move_index[1]] < 0:
                index.append([i, j])
    for i in index:
        valid_moves = valid(piece_lookup(i), i)
        escape_moves += check_check(valid_moves,i)
    if not escape_moves:
        return True
    else:
        return False

#compares user move to valid moves
def compare(valid_moves,move_index):
    if move_index in valid_moves:
        return True

#converts chess index to list index
def num_to_index(num):
    for i in range(8):
        for j in range(8):
            if board_num[i][j] == num:
                index = [i,j]
                return index
    else:
        return [10,10]

def move_rook(move_index):
    #queenside
    if move_index[1] == 2:
        update_board([move_index[0],0],[move_index[0],3],False)
    #kingside
    else: #move_index[1] == 6:
        update_board([move_index[0],7],[move_index[0],5], False)
    return
