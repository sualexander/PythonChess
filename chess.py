from pieces import *

#draws board
def print_board(white_move):
    if white_move:
        print("white to move")
    else:
        print("black to move")
    num_to_display ={1: "W\u265C",2: "W\u265E",3: "W\u265D",4: "W\u265B",5: "W\u265A",6: "W\u265F",-1: "B\u265C",-2: "B\u265E",-3: "B\u265D",-4: "B\u265B",-5: "B\u265A",-6: "B\u265F"}
    for i in range(8):
        row_pic = []
        for j in range(8):
            pic = num_to_display.get(board.chess_board[i][j], "--")
            row_pic.append(pic)
        print(row_pic)
#converts chess index to list index
def num_to_index(num):
    for i in range(8):
        for j in range(8):
            if board_num[i][j] == num:
                index = [i,j]
                return index
    else:
        return [10,10]
#converts move index to piece name at target square
def piece_lookup(piece_index):
    for i in range(8):
        for j in range(8):
            if [i,j] == piece_index:
                piece_abrv = board.chess_board[i][j]
                names = {6: 'pawn', 1: 'rook', 2: 'knight', 3: 'bishop', 4: 'queen', 5: 'king'}
                piece_name = names.get(abs(piece_abrv), "none")
                return piece_name
    return "none"
#gets list of valid moves
def valid(piece_name, piece_index):
    if piece_name != "none":
        return remove_negative(globals()[piece_name](piece_index))
    else:
        print("invalid selection")
        return
def remove_negative(valid_moves):
    temp_moves = valid_moves.copy()
    for i in valid_moves:
        if i[0] < 0 or i[1] < 0:
            temp_moves.remove(i)
        elif i[0] > 7 or i[1] > 7:
            temp_moves.remove(i)
    valid_moves = temp_moves
    return valid_moves
#modifies valid_moves so that a move cannot lead to check
def check_check(valid_moves,piece_index):
    index = []
    for i in range(8):
        for j in range(8):
            if board.chess_board[i][j] * board.chess_board[piece_index[0]][piece_index[1]] < 0:
                index.append([i, j])
            elif abs(board.chess_board[i][j]) == 5:
                king = [i, j]
    temp_moves = valid_moves.copy()
    temp_index = king
    for x in valid_moves:
        if piece_index == temp_index:
            king = x
        temp = board.chess_board[x[0]][x[1]]
        board.chess_board[x[0]][x[1]] = board.chess_board[piece_index[0]][piece_index[1]]
        board.chess_board[piece_index[0]][piece_index[1]] = 0

        for i in index:
            valid_squares = valid(piece_lookup(i), i)
            if king in valid_squares:
                temp_moves.remove(x)
                break
        board.chess_board[piece_index[0]][piece_index[1]] = board.chess_board[x[0]][x[1]]
        board.chess_board[x[0]][x[1]] = temp

    valid_moves = temp_moves
    valid_moves = remove_negative(valid_moves)
    return valid_moves
#compares user move to valid moves
def compare(valid_moves,move_index):
    if move_index in valid_moves:
        return True
def deliver_check(move_index):
    index = []
    for i in range(8):
        for j in range(8):
            if board.chess_board[i][j] * board.chess_board[move_index[0]][move_index[1]] > 0:
                index.append([i, j])
            elif abs(board.chess_board[i][j]) == 5:
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
            if board.chess_board[i][j] * board.chess_board[move_index[0]][move_index[1]] < 0:
                index.append([i, j])
    for i in index:
        valid_moves = valid(piece_lookup(i), i)
        escape_moves += check_check(valid_moves,i)
    if not escape_moves:
        return True
    else:
        return False

#updates board
def update_board(board,piece_index,move_index,promotion):
    #pawn promotion
    if promotion:
        abrv = pawn_promotion(piece_index)
    else:
        abrv = board[piece_index[0]][piece_index[1]]
    #en passant
    board.past_move = [piece_index,move_index]
    #checks if user has moved rooks or king or if rooks has been captured for castling
    if board.chess_board[piece_index[0]][piece_index[1]] > 0:
        if abrv == 5:
            board.wcan_castle = [0,0]
        elif (abrv == 1 and piece_index[1] == 0) or (board.chess_board[7][0] != 1):
            board.wcan_castle[0] = 0
        elif (abrv == 1 and piece_index[1] == 7) or (board.chess_board[7][7] != 1):
            board.wcan_castle[1] = 0
    else:
        if abrv == -5:
            board.bcan_castle = [0,0]
        elif (abrv == -1 and piece_index[1] == 0) or (board.chess_board[0][0] != -1):
            board.bcan_castle[0] = 0
        elif (abrv == -1 and piece_index[1] == 7) or (board.chess_board[0][7] != -1):
            board.bcan_castle[1] = 0
    #modifies board with player move
    board.chess_board[move_index[0]][move_index[1]] = abrv
    board.chess_board[piece_index[0]][piece_index[1]] = 0

def move_rook(move_index):
    #queenside
    if move_index[1] == 2:
        update_board(board.chess_board,[move_index[0],0],[move_index[0],3],False)
    #kingside
    else: #move_index[1] == 6:
        update_board([board.chess_board,move_index[0],7],[move_index[0],5], False)
    return
def castle(piece_index):
    valid_moves = []
    if board.chess_board[piece_index[0]][piece_index[1]] > 0:
        xcan_castle = board.wcan_castle
    else:
        xcan_castle = board.bcan_castle
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
        if board.chess_board[piece_index[0]][piece_index[1]+(i+1)*n] != 0:
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
def pawn_promotion(piece_index):
    not_valid = True
    while not_valid:
        promote = input("promote?")
        if (promote == "y") or (promote == "yes"):
            not_valid = False
            piece = input("queen, rook, bishop, knight")
            names = {'rook': 1, 'knight': 2, 'bishop': 3, 'queen': 4}
            if board.chess_board[piece_index[0]][piece_index[1]] > 0:
                abrv = names.get(piece, "none")
            else:
                abrv = -names.get(piece, "none")
            if abrv == "none":
                print("invalid selection")
                not_valid = True
        elif (promote == "n") or (promote == "no"):
            not_valid = False
            if board.chess_board[piece_index[0]][piece_index[1]] > 0:
                abrv = board.chess_board[piece_index[0]][piece_index[1]]
            else:
                abrv = board.chess_board[piece_index[0]][piece_index[1]]
            if abrv == "none":
                print("invalid selection")
                not_valid = True
        else:
            print("invalid selection")
            not_valid = True
    return abrv
def en_passant(piece_index):
    valid_moves = []
    if board.past_move[0][0] == 1:
        n = 1
    else:
        n = -1
    if [piece_index[0],piece_index[1] - 1] == board.past_move[1]:
        valid_moves.append([board.past_move[1][0] -1*n,board.past_move[1][1]])
    if [piece_index[0],piece_index[1] + 1] == board.past_move[1]:
        valid_moves.append([board.past_move[1][0] -1*n,board.past_move[1][1]])
    return valid_moves