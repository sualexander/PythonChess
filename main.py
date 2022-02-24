import chess
import computer

if __name__ == "__main__":
    chess.make_boards()
    chess.start_game()

running = True
white_move = True
while running:
    board = chess.update_game(white_move)
    white_move = not white_move
    white_move = computer.update_move(board,white_move)