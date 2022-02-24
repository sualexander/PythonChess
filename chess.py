#creates starting chess board and array of associated square names
def make_boards():
    global board_num, board
    board = []
    row_pieces = [1, 2, 3, 4, 5, 3, 2, 1]
    for i in range(16):
        board.append([0 for j in range(16)])
    for i in range(8):
        board[7][i] = row_pieces[i]
        board[0][i] = -row_pieces[i]
        board[1][i] = -6
        board[6][i] = 6

    board_num = []
    for i in range(8):
        board_num.append([chr(97+j) + str(8-i) for j in range(8)])

#starts while loop
def start_game():
    global wcan_castle, bcan_castle, past_move
    wcan_castle = [1,1]
    bcan_castle = [1,1]
    past_move = [[10,10],[10,10]] #arbitrary declaration not in board

def update_game(white_move):
    if white_move:
        print("white to move")
    else:
        print("black to move")
    print_board()
    valid_move = True
    while valid_move:
        valid_move = update_move(white_move)
    return board

#draws board
def print_board():
    num_to_display ={1: "W\u265C",2: "W\u265E",3: "W\u265D",4: "W\u265B",5: "W\u265A",6: "W\u265F",-1: "B\u265C",-2: "B\u265E",-3: "B\u265D",-4: "B\u265B",-5: "B\u265A",-6: "B\u265F"}
    for i in range(8):
        row_pic = []
        for j in range(8):
            pic = num_to_display.get(board[i][j], "--")
            row_pic.append(pic)
        print(row_pic)

#asks user for move and evaluates validity of move
def update_move(white_move):
    piece = input("which piece?") #example: e4
    piece_index = num_to_index(piece)
    if (board[piece_index[0]][piece_index[1]] < 0) == white_move:
        print("wrong color")
        return True
    piece_name = piece_lookup(piece_index)
    #returns array of allowed moves based on type of selected piece
    valid_moves = valid(piece_name,piece_index)
    if not valid_moves:
        print("no valid moves")
        return True
    #en passant
    en_passant_squares = []
    if piece_name == "pawn":
        en_passant_squares = en_passant(piece_index)
        valid_moves += en_passant_squares
    #checks if move would allow discovered check
    valid_moves = check_check(valid_moves,piece_index)
    #adds castling moves to valid_moves if allowed
    castle_squares = []
    if piece_name == "king":
        castle_squares = castle(piece_index)
        valid_moves += castle_squares
    if not valid_moves:
        print("no valid moves")
        return True

    move = input("enter your move")
    
    move_index = num_to_index(move)
    if compare(valid_moves, move_index):
        #pawn promotion
        if (piece_name == "pawn") and ((move_index[0] == 0) or (move_index[0] == 7)):
            promotion = True
        else:
            promotion = False
        #en passant
        if move_index in en_passant_squares:
            board[past_move[1][0]][past_move[1][1]] = 0
        #castling
        elif move_index in castle_squares:
            move_rook(move_index)
        update_board(piece_index,move_index,promotion)
        if deliver_check(move_index):
            if check_mate(move_index):
                #check for draw
                if check_mate(move_index*-1):
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

def remove_negative(valid_moves):
    temp_moves = valid_moves.copy()
    for i in valid_moves:
        if i[0] < 0 or i[1] < 0:
            temp_moves.remove(i)
        elif i[0] > 7 or i[1] > 7:
            temp_moves.remove(i)
    valid_moves = temp_moves
    return valid_moves

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

#gets list of valid moves
def valid(piece_name, piece_index):
    if piece_name != "none":
        return remove_negative(globals()[piece_name](piece_index))
    else:
        print("invalid selection")
        return
#compares user move to valid moves
def compare(valid_moves,move_index):
    if move_index in valid_moves:
        return True
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
#converts chess index to list index
def num_to_index(num):
    for i in range(8):
        for j in range(8):
            if board_num[i][j] == num:
                index = [i,j]
                return index
    else:
        return [10,10]

###########################################
#checks valid moves for each type of piece

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

def move_rook(move_index):
    #queenside
    if move_index[1] == 2:
        update_board([move_index[0],0],[move_index[0],3],False)
    #kingside
    else: #move_index[1] == 6:
        update_board([move_index[0],7],[move_index[0],5], False)
    return

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


