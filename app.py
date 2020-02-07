import numpy as np
from itertools import groupby

ROWS = 6
COLUMNS = 7
WIN_ELEMENTS = 3
PLAYERS = {"X": "Игрок № 1", "O": "Игрок № 2"}


class ItemsBoard:

    __slots__ = ["_rows", "_columns", "_np_cells"]

    def __init__(self, rows: int, columns: int, cells_range: list):

        self._rows = rows
        self._columns = columns
        self._np_cells = np.array(cells_range, dtype=object).reshape(rows, columns)

    @property
    def rows(self):
        return self._rows

    @property
    def columns(self):
        return self._columns

    @property
    def cells(self):
        return self._np_cells

    def get_item(self, i, j):
        return self._np_cells[i][j]

    #  with gravity
    def set_item(self, j, marker):
        column = j
        for i in range(self._rows):

            #  check cell is empty ""
            if self._np_cells[i][column]:
                self._np_cells[i - 1][column] = marker
                return True

        self._np_cells[self._rows - 1][column] = marker

    def get_empty(self, column: int):
        for i in range(self._rows):
            if not self._np_cells[i][column]:
                return True


class Board:
    __slots__ = ["rows", "columns"]

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns

    def draw_board(self, items_board):
        header = ""
        for co_numb in range(self.columns):
            header += f"|\t{co_numb}\t"
        print(header + "|")
        columns_row = ""
        print(f"{'-' * 60}")
        for i in range(self.rows):
            for j in range(self.columns):
                columns_row += f"|\t{items_board.get_item(i, j)}\t"
            columns_row += f"|\n{'-' * 60}\n"
        print(columns_row)


def take_input(marker: str, item_board: object):
    valid = False
    while not valid:
        player_answer = input(f"Куда поставим {marker}? (укажите номер столбца)")

        try:
            player_answer = int(player_answer)
        except ValueError:
            print("Некорректный ввод. Я принимаю только целые числа!")
            continue

        min = 0
        max = item_board.rows

        if min <= player_answer <= max:
            if item_board.get_empty(player_answer):
                column = player_answer
                item_board.set_item(column, marker)
                valid = True
            else:
                print("Эта клеточка уже занята")
        else:
            print(f"Введите число в диапазоне  от {min}  до {max}, чтобы походить.")


def check_win(items_board: object, marker: str, win_lenght: int, players: dict):
    rows = item_board.rows
    columns = item_board.columns
    matrix = items_board.cells

    # check for row
    for idx in range(rows):
        lst = matrix[idx, :]
        if list_sum(lst, marker, win_lenght) == "ok":
            print("Победил: ", players[marker])
            return True

    # check for column
    for idx in range(columns):
        lst = matrix[:, idx]
        if list_sum(lst, marker, win_lenght) == "ok":
            print("Победил: ", players[marker])
            return True

    diags = [matrix[::-1, :].diagonal(i) for i in range(-rows + 1, columns)]
    diags.extend(matrix.diagonal(i) for i in range(-rows + 1, columns))

    #  check for diagonalls
    for row in diags:
        if list_sum(row, marker, win_lenght) == "ok":
            print("Победил: ", players[marker])
            return True


def list_sum(row, marker, lenght):
    for key, group in groupby(row):
        if key == marker:
            sequence = list(group)
            if len(sequence) == lenght:
                return "ok"


if __name__ == "__main__":

    cells = int(ROWS * COLUMNS)
    cells_range = ["" for i in range(cells)]
    item_board = ItemsBoard(rows=ROWS, columns=COLUMNS, cells_range=cells_range)
    board = Board(rows=ROWS, columns=COLUMNS)

    flag = True
    counter = 0
    try:
        while flag:

            board.draw_board(item_board)

            if counter % 2 == 0:
                marker = "X"
                print("Ход игрока № 1:")
                take_input(marker, item_board)
            else:
                print("Ход игрока № 2:")
                marker = "O"
                take_input(marker, item_board)

            temp = check_win(item_board, marker, WIN_ELEMENTS, players=PLAYERS)
            if temp:
                break
            if counter == cells:
                print("Ничья!")
                break
            counter += 1
        board.draw_board(item_board)

    except KeyboardInterrupt:
        print("\nИгра преждевременно остановлена!")
