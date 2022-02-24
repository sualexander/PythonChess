#creates starting chess board and array of associated square names
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
    board_num.append([chr(97 + j) + str(8 - i) for j in range(8)])

wcan_castle = [1, 1]
bcan_castle = [1, 1]
past_move = [[10, 10], [10, 10]]  # arbitrary declaration not in board