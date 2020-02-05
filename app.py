from itertools import chain

ROWS = 6
COLUMNS = 7


class ItemsBoard:

    __slots__ = ["_cells"]

    def __init__(self, rows, columns):

        self._cells = list(range(rows * columns))

    @property
    def cells(self):
        return self._cells

    def get_item(self, i):
        return self._cells[i]

    def set_item(self, i, item):
        self._cells[i] = item


class Board:

    __slots__ = ["rows", "columns", "cells"]

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.cells = rows * columns

    def draw_board(self, items_board):
        columns_row = ""
        print(f"{'-' * 60}")
        for i in range(0, self.cells, self.columns):
            for j in range(0, self.columns):
                item_index = i + j
                columns_row += f"|\t{items_board.get_item(item_index)}\t"
            columns_row += f"|\n{'-' * 60}\n"
        print(columns_row)


def take_input(player_token: str, items: object):
    valid = False
    while not valid:
        player_answer = input("Куда поставим " + player_token+"? ")

        try:
            player_answer = int(player_answer)
        except ValueError:
            print("Некорректный ввод. Я принимаю только целые числа!")
            continue

        if 0 <= player_answer <= 41:

            if str(items.get_item(player_answer))not in "XO":
                items.set_item(player_answer, player_token)
                valid = True
            else:
                print("Эта клеточка уже занята")
        else:
            print("Некорректный ввод. Введите число от 0 до 41 чтобы походить.")


def coord(cells, step):
    """Calculates winning coordinates

    :param cells: number cells
    :param step: step is equivalent number  of columns
    :return: list with winning coordinates
    """

    win_lst = []

    # horizontal winning values
    win_coord_1 = [(i, i + 1, i + 2, i + 3) for n in range(0, cells, step) for i in range(n, n + 4)]

    # vertical winning values
    win_coord_2 = [(i, i + 7, i + 14, i + 21) for n in range(0, 15, step) for i in range(n, n + 7)]

    # victory values on the left diagonal
    win_coord_3 = [(i, i + 8, i + 16, i + 24) for n in range(0, 15, step) for i in range(n, n + 4)]

    # victory values on the right diagonal
    win_coord_4 = [(i, i + 6, i + 12, i + 18) for n in range(3, 22, step) for i in range(n, n + 4)]

    for i in range(1, 5):
        win_lst.append((eval(f"win_coord_{i}")))
    win_lst = list(chain(*win_lst))
    return win_lst


def check_win(items_board: object, win_coord: list):
    board = items_board.cells
    for each in win_coord:
        if board[each[0]] == board[each[1]] == board[each[2]] == board[each[3]]:
            if board[each[0]] == "X":
                return "Игрок 1 выиграл!"
            return "Игрок 2 выиграл!"
    return False


if __name__ == "__main__":
    cells = int(ROWS * COLUMNS)
    win_board = coord(cells=cells, step=COLUMNS)
    item_board = ItemsBoard(rows=ROWS, columns=COLUMNS)
    board = Board(rows=ROWS, columns=COLUMNS)
    flag = True
    counter = 0
    try:
        while flag:
            board.draw_board(item_board)

            if counter % 2 == 0:
                print("Ход игрока № 1:")
                take_input("X", item_board)
            else:
                print("Ход игрока № 2:")
                take_input("O", item_board)
            counter += 1
            if counter > 6:
                tmp = check_win(item_board, win_coord=win_board)
                if tmp:
                    print(tmp)
                    break
            if counter == cells:
                print("Ничья!")
                break
        board.draw_board(item_board)
    except KeyboardInterrupt:
        print("\nИгра преждевременно остановлена!")
