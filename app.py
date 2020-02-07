import numpy as np
from itertools import groupby
from sys import argv

# ROWS = 6
# COLUMNS = 7
# WIN_ELEMENTS = 4
try:
    ROWS = int(argv[1])
    COLUMNS = int(argv[2])
    WIN_ELEMENTS = int(argv[3])
except ValueError:
    raise ValueError("Значения должны быть целочисленными!")
    

PLAYERS = {"X": "Игрок № 1", "O": "Игрок № 2"}


class CellItems:

    __slots__ = ("_rows", "_columns", "_np_cells")

    def __init__(self, rows: int, columns: int, cells_lst: list):
        self._rows = rows
        self._columns = columns
        self._np_cells = np.array(cells_lst, dtype=object).reshape(rows, columns)

    @property
    def rows(self):
        return self._rows

    @property
    def columns(self):
        return self._columns

    @property
    def cells(self):
        return self._np_cells

    def get_item(self, i: int, j: int):
        return self._np_cells[i][j]

    #  with gravity
    def set_item(self, j: int, marker: str) -> bool:
        column = j
        for i in range(self._rows):

            #  check cell is empty ""
            if self._np_cells[i][column]:
                self._np_cells[i - 1][column] = marker
                return True

        self._np_cells[self._rows - 1][column] = marker

    # return True if cell is empty
    def get_empty(self, column: int) -> bool:
        for i in range(self._rows):
            if not self._np_cells[i][column]:
                return True


class Board(CellItems):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def draw_board(self):

        header = ""
        for co_numb in range(self._columns):
            header += f"|\t{co_numb}\t"
        print(header + "|")
        columns_row = ""
        print(f"{'-' * self._columns * 2 *8}")
        for i in range(self._rows):
            for j in range(self._columns):
                columns_row += f"|\t{super().get_item(i, j)}\t"
            columns_row += f"|\n{'-' * self._columns * 2 * 8}\n"
        print(columns_row)


def take_input(marker: str, board: object):
    valid = False
    while not valid:
        player_answer = input(f"Куда поставим {marker}? (укажите номер столбца)")

        try:
            player_answer = int(player_answer)
        except ValueError:
            print("Некорректный ввод. Я принимаю только целые числа!")
            continue

        min = 0
        max = board.rows

        if min <= player_answer <= max:
            if board.get_empty(player_answer):
                column = player_answer
                board.set_item(column, marker)
                valid = True
            else:
                print("Эта клеточка уже занята")
        else:
            print(f"Введите число в диапазоне  от {min}  до {max}, чтобы походить.")


def check_win(board: object, marker: str, win_lenght: int, players: dict):
    rows = board.rows
    columns = board.columns
    matrix = board.cells

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
    cells_lst = ["" for i in range(cells)]
    board = Board(rows=ROWS, columns=COLUMNS, cells_lst=cells_lst)

    flag = True
    counter = 0
    try:
        while flag:

            board.draw_board()
            if counter % 2 == 0:
                marker = "X"
                print("Ход игрока № 1:")
                take_input(marker, board)
            else:
                print("Ход игрока № 2:")
                marker = "O"
                take_input(marker, board)

            temp = check_win(board, marker, WIN_ELEMENTS, players=PLAYERS)
            if temp:
                break
            if counter == cells:
                print("Ничья!")
                break
            counter += 1
        board.draw_board()

    except KeyboardInterrupt:
        print("\nИгра преждевременно остановлена!")
