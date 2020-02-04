import copy
from itertools import chain

NUMBER = 43
# NUMBER = 10

board = list(range(1, NUMBER))

print(board)


def draw_board(board, rows, columns):
    print(f"{'-'*30}")
    columns_row = ""
    for i in range(0, 42, 7):
        for j in range(0, 7, 1):
            columns_row += f"|{board[i + j]}\t"
        columns_row += f"|\n{'-'*30}\n"
    print(columns_row)


def take_input(player_token):
    valid = False
    while not valid:
        player_answer = input("Куда поставим " + player_token+"? ")
        try:
            player_answer = int(player_answer)
        except:
            print ("Некорректный ввод. Вы уверены, что ввели число?")
            continue
        if 1 <= player_answer <= 42:
            if (str(board[player_answer-1]) not in "XO"):
                board[player_answer-1] = player_token
                valid = True
            else:
                print("Эта клеточка уже занята")
        else:
            print("Некорректный ввод. Введите число от 1 до 42 чтобы походить.")


def coord(board, win=[]):
    win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    win_coord_1 = ((i, i + 1, i + 2, i + 3) for i in range(0, 4, 1))
    win_coord_2 = ((i, i + 1, i + 2, i + 3) for i in range(7, 11, 1))
    win_coord_3 = ((i, i + 1, i + 2, i + 3) for i in range(14, 18, 1))
    win_coord_4 = ((i, i + 1, i + 2, i + 3) for i in range(21, 25, 1))
    win_coord_5 = ((i, i + 1, i + 2, i + 3) for i in range(28, 32, 1))
    win_coord_6 = ((i, i + 1, i + 2, i + 3) for i in range(35, 39, 1))

    win_coord_7 = ((i, i + 7, i + 14, i + 21) for i in range(0, 7))
    win_coord_8 = ((i + 7, i + 14, i + 21, i + 28) for i in range(0, 7))
    win_coord_9 = ((i + 14, i + 21, i + 28, i + 36) for i in range(0, 7))

    for i in range(1, 9):
        win.append(tuple(eval(f"win_coord_{i}")))
    win = list(chain(*win))
    print("win", win)
    return win


def check_win(board, win_coord):
    print("len", len(win_coord))
    for each in win_coord:
        if board[each[0]] == board[each[1]] == board[each[2]] == board[each[3]]:
            return board[each[0]]
    return False


def main(board):
    counter = 0
    win = False
    while not win:
        draw_board(board, rows=6, columns=7)
        if counter % 2 == 0:
            print("Игрок 1")
            take_input("X")
        else:
            print("Игрок 2")
            take_input("O")
        counter += 1
        if counter > 1:
            win_coord = coord(board)
            tmp = check_win(board, win_coord=win_coord)
            if tmp:
                print(tmp, "выиграл!")
                win = True
                break
        if counter == 9:
            print("Ничья!")
            break
    draw_board(board, rows=6, columns=7)


main(board)