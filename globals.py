from dataclasses import dataclass

#creates starting chess_board and array of associated square names
@dataclass
class Board:
    chess_board: list
    wcan_castle: list
    bcan_castle: list
    past_move: list

board = Board([],[1, 1],[1, 1],[[10, 10], [10, 10]])
row_pieces = [1, 2, 3, 4, 5, 3, 2, 1]
for i in range(16):
    board.chess_board.append([0 for j in range(16)])
for i in range(8):
    board.chess_board[7][i] = row_pieces[i]
    board.chess_board[0][i] = -row_pieces[i]
    board.chess_board[1][i] = -6
    board.chess_board[6][i] = 6

#corresponding array of square names eg: e4
board_num = []
for i in range(8):
    board_num.append([chr(97 + j) + str(8 - i) for j in range(8)])

print(board.chess_board)



