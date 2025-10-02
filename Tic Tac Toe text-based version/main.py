from numpy import random

# At first all sockets are empty, then the player is first (X), and the bot is second (0)
current_player = 'X'
move_count = 0
board_data = [' '] * 9

def print_board ():
    print()
    print(f"{board_data[0]} | {board_data[1]} | {board_data[2]}")
    print("--+---+--")
    print(f"{board_data[3]} | {board_data[4]} | {board_data[5]}")
    print("--+---+--")
    print(f"{board_data[6]} | {board_data[7]} | {board_data[8]}")
    print()



def is_full():
    if move_count == 9:
        print("We have a draw here.")
        return True
    return False

def print_result(winner):
    if winner == 1 :
        print("You are a winner.")
    else :
        print("You lost. Bot has won!!!")

def check_winner ():
    # check 3 rows
    for row in range(3) :
        if board_data[3*row] == board_data[3*row + 1] == board_data[3*row + 2]!= ' ' :
            if board_data[3*row] == current_player :
                print_result(1)
            else :
                print_result(2)
            return True

    #check 3 columns
    for column in range(3) :
        if board_data[column] == board_data[column+3] == board_data[column + 6] != ' ' :
            if board_data[column] == current_player :
                print_result(1)
            else :
                print_result(2)
            return True

    # check main diagonal
    if board_data[0] == board_data[4] == board_data[8] != ' ':
        if board_data[0] == current_player:
            print_result(1)
        else:
            print_result(2)
        return True

    # check second diagonal
    if board_data[2] == board_data[4] == board_data[6] != ' ':
        if board_data[2] == current_player:
            print_result(1)
        else:
            print_result(2)
        return True

    return False

def check_empty(row, column):
    if board_data[3*row + column] != ' ' :
        return False
    return True

def human_move ():
    print(f"Choose where to put {current_player} on a board.")
    print(f"Inter a row where to put {current_player} (1 to 3) that is empty: ")
    move_row = int(input()) - 1
    print(f"Inter a row where to put {current_player} (1 to 3) that is empty: ")
    move_column = int(input()) - 1
    if not check_empty(move_row, move_column):
        print(f"Position ({move_row+1},{move_column+1})that you choose is already taken. Try again.")
        print("")
        human_move()
    else :
        board_data[3 * move_row + move_column] = current_player



def bot_generate_position(number_of_empty_space):
    position_in_empty_space = random.randint(number_of_empty_space - 1) + 1
    empty_space_position = 0
    for i in range(9):
        if board_data[i] == ' ':
            empty_space_position += 1

        if position_in_empty_space == empty_space_position:
            return i


def bot_move():
    position = bot_generate_position(9 - move_count)
    if current_player == 'X' :
        board_data[position] = '0'
    else :
        board_data[position] = 'X'

while True:
    print_board()
    if move_count%2 == 0 :
        if current_player == 'X':
            human_move()
        else :
            bot_move()
    else :
        if current_player != 'X':
            human_move()
        else :
            bot_move()

    move_count += 1

    if check_winner():
       break

    if is_full():
        break