import numpy as np
from itertools import chain

ROWS = 6
COLUMNS = 7
WIN_ELEMENTS = 4


class ItemsBoard:

    __slots__ = ["rows", "columns", "np_cells"]

    def __init__(self, rows: int, columns: int, cells_range: list):

        self.rows = rows
        self.columns = columns
        self.np_cells = np.array(cells_range, dtype=object).reshape(rows, columns)

    @property
    def cells(self):
        return self.np_cells

    def get_item(self, i, j):
        return self.np_cells[i][j]

    def set_item(self, i, j, item):
        print(self.np_cells[i][j])
        self.np_cells[i][j] = item

    def get_indexs(self, item: int):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.np_cells[i][j] == item:
                    return i, j


class Board:

    __slots__ = ["rows", "columns"]

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns

    def draw_board(self, items_board):
        columns_row = ""
        print(f"{'-' * 60}")
        for i in range(self.rows):
            for j in range(self.columns):
                columns_row += f"|\t{items_board.get_item(i, j)}\t"
            columns_row += f"|\n{'-' * 60}\n"
        print(columns_row)


def take_input(player_token: str, item_board: object):
    valid = False
    while not valid:
        player_answer = input("Куда поставим " + player_token + "? ")

        try:
            player_answer = int(player_answer)
        except ValueError:
            print("Некорректный ввод. Я принимаю только целые числа!")
            continue

        if 0 <= player_answer <= 41:
            try:
                i, j = item_board.get_indexs(player_answer)

            except (ValueError, TypeError):
                print("Эта клеточка уже занята")
            else:
                item_board.set_item(i, j, player_token)
                valid = True
        else:
            print("Некорректный ввод. Введите число от 0 до 41 чтобы походить.")


def win_coordinates(rows, columns, lenght):
    # horizontal winning values
    _cells = int(rows * columns)

    def horizontal():
        nonlocal _cells, lenght
        main_lst = []
        worker_lst = []
        for item in range(_cells):
            worker_lst.append(item)

            if len(worker_lst) == lenght:
                print(worker_lst)
                main_lst.append(worker_lst)
                worker_lst = []

        return main_lst

    return horizontal()



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

    cells_range = list(range(cells))
    item_board = ItemsBoard(rows=ROWS, columns=COLUMNS, cells_range=cells_range)
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


