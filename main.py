import human
import computer

running = True
#ask pvp or pvcomputer
white_move = True


while running:

    human.update_game(white_move)
    white_move = not white_move

    computer.update_game(white_move)
    white_move = not white_move


