import numpy as np
from itertools import groupby

ROWS = 6
COLUMNS = 7
WIN_ELEMENTS = 4
PLAYERS = {"X": "Игрок № 1", "O": "Игрок № 2"}


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

    #  without gravity
    # def set_item(self, i, j, item):
    #     print(self.np_cells[i][j])
    #     self.np_cells[i][j] = item

    #  with gravity
    def set_item(self, j, marker):
        const = j
        for i in range(self.rows):
            if self.np_cells[i][const] == "X" or self.np_cells[i][const] == "O":
                self.np_cells[i - 1][const] = marker
                return True
            else:
                continue
        self.np_cells[self.rows - 1][const] = marker


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
                item_board.set_item(j, player_token)
                valid = True
        else:
            print("Некорректный ввод. Введите число от 0 до 41 чтобы походить.")


class ChechWin:

    def __init__(self, items_board: object, marker:str, win_lenght: int, players: dict):

        self.i_b = items_board.cells
        self.win_lenght = win_lenght
        self.players = players

    def check_row(self, i_b, marker):
        for row in enumerate(i_b):
            if listSum(row[1], marker, self.win_lenght) == "ok":
                print("Winner:", self.players[marker])
                return True

    def check_column(self, i_b, marker):
        for index, _ in enumerate(i_b[0]):
            if listSum(i_b[:, index], marker, self.win_lenght) == "ok":
                print("Winner:", self.players[marker])
                return True


def check_win(items_board: object, marker: str, win_lenght: int, players: dict):
    i_b = items_board.cells

    # check for row
    for row in enumerate(i_b):
        if listSum(row[1], marker, win_lenght) == "ok":
            print("Winner:", players[marker])
            return True

    # check for column
    for index, _ in enumerate(i_b[0]):
        if listSum(i_b[:, index], marker, win_lenght) == "ok":
            print("Winner:", players[marker])
            return True

    # create diagonaly
    max_col = len(i_b)
    max_row = len(i_b[0])
    min_bdiag = -max_col + 1
    fdiag = [[] for i in range(max_col + max_row - 1)]
    bdiag = [[] for i in range(len(fdiag))]
    for y in range(max_col):
        for x in range(max_row):
            fdiag[x + y].append(i_b[y][x])
            bdiag[-min_bdiag + x - y].append(i_b[y][x])

    #  check for diagonally
    for row in fdiag:
        if listSum(row, marker, win_lenght) == "ok":
            print("Победил: ", players[marker])
            return True

    # check for diagonally
    for row in bdiag:
        if listSum(row, marker, win_lenght) == "ok":
            print("Победил: ", players[marker])
            return True


def listSum(row, marker, lenght):
    for key, group in groupby(row):
        if key == marker:
            sequence = list(group)
            if len(sequence) == lenght:
                return "ok"


if __name__ == "__main__":
    cells = int(ROWS * COLUMNS)
    cells_range = list(range(cells))
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
            # if counter > WIN_ELEMENTS:
            temp = check_win(item_board, marker, WIN_ELEMENTS, players=PLAYERS)
            if temp:
                break
            counter += 1
            if counter == cells:
                print("Ничья!")
                break
        board.draw_board(item_board)
    except KeyboardInterrupt:
        print("\nИгра преждевременно остановлена!")


