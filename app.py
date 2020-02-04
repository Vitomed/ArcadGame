import copy

NUMBER = 43
# NUMBER = 10

board = list(range(1, NUMBER))

print(board)


def draw_board(board, rows, columns):
    print(f"\t{'-'*25}")
    columns_row = "\t | "
    for i in range(0, 42, 7):
        for j in range(0, 7, 1):
            columns_row += f"{board[i + j]}|"
        columns_row += f"\n\t{'-'*25}\n\t"
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

def check_win(board):
    win_coord = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
    for each in win_coord:
        if board[each[0]] == board[each[1]] == board[each[2]]:
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
        if counter > 4:
            tmp = check_win(board)
            if tmp:
                print(tmp, "выиграл!")
                win = True
                break
        if counter == 9:
            print("Ничья!")
            break
    draw_board(board, rows=6, columns=7)


main(board)