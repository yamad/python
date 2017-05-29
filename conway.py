#!/usr/bin/env python3
""" Conway's Game of Life

@author Jason Yamada-Hanff
@date 2017-05-28
"""
import curses
import random


def live_or_die(bitstate, neighbor_count):
    """Standard rules for Conway's Game of Life"""
    if neighbor_count >= 4: return 0  # overpopulation
    if neighbor_count <= 1: return 0  # loneliness
    if neighbor_count == 3: return 1  # birth (if dead)
    return bitstate                   # stasis, passthrough


def game_of_life(initial=None):
    """Return generator for Conway's Game of Life"""
    state = initial or [[0] * 5] * 5
    nrows, ncols = len(state), len(state[0])

    def live_neighbors(i, j, nrows, ncols):
        # sum neighbor grid, max/min handles edge cells
        grid_sum = sum(state[x][y]
                       for x in range(max(i-1, 0), min(i+2, nrows))
                       for y in range(max(j-1, 0), min(j+2, ncols)))
        return grid_sum - state[i][j]  # don't count own cell

    while True:
        yield state
        state = [[live_or_die(bit, live_neighbors(i, j))
                  for j, bit in enumerate(row)]
                 for i, row in enumerate(state)]


def game_of_life_wraparound(initial=None):
    """Return Conway's Game of Life generator, with wraparound on edges"""
    state = initial or [[0] * 5] * 5
    nrows, ncols = len(state), len(state[0])

    def live_neighbors_wrap(i, j):
        # sum neighbor grid, wraparound edges
        grid_sum = sum(state[ii][jj]
                       for ii in [(i-1) % nrows, i, (i+1) % nrows]
                       for jj in [(j-1) % ncols, j, (j+1) % ncols])
        return grid_sum - state[i][j]  # don't count own cell

    while True:
        yield state
        state = [[live_or_die(s, live_neighbors_wrap(i, j))
                  for j, s in enumerate(row)]
                 for i, row in enumerate(state)]


def edgepad_board(board, left=1, right=1, top=1, bottom=1):
    """Return board with lines of 0-padding on left/right/top/bottom"""
    ncols = len(board[0])
    left_pad = [0] * left
    right_pad = [0] * right
    top_row = [left_pad + ([0] * ncols) + right_pad]
    top_pad = top_row * top
    bottom_pad = top_row * bottom
    pad_rows = [(left_pad + row + right_pad) for row in board]
    return top_pad + pad_rows + bottom_pad


def run(initial):
    def display(board):
        lines = ["".join("*" if s else " " for s in row) for row in board]
        return "\n".join(lines)

    game = game_of_life(initial)
    for move in game:
        print(display(move))


def random_board(height, width):
    """Return random board state with given height and width"""
    return [[random.choice([0, 1])
             for _ in range(width)]
            for _ in range(height)]


block = [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]

blinker = [[0, 0, 0, 0, 0],
           [0, 0, 1, 0, 0],
           [0, 0, 1, 0, 0],
           [0, 0, 1, 0, 0],
           [0, 0, 0, 0, 0]]

beacon = [[0, 0, 0, 0, 0, 0],
          [0, 1, 1, 0, 0, 0],
          [0, 1, 0, 0, 0, 0],
          [0, 0, 0, 0, 1, 0],
          [0, 0, 0, 1, 1, 0],
          [0, 0, 0, 0, 0, 0]]

glider = [[0, 0, 1, 0, 0, 0],
          [0, 0, 0, 1, 0, 0],
          [0, 1, 1, 1, 0, 0],
          [0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0]]


### curses interface

def display_curses(screen, board, yoff, xoff):
    for y, row in enumerate(board):
        for x, bit in enumerate(row):
            if bit:
                screen.addstr(y+yoff, x+xoff, "*")

def run_curses(stdscr):
    curses.curs_set(0)          # hide cursor
    curses.halfdelay(2)         # allow input, setup refresh rate
    curses.noecho()             # don't print inputs

    initial = random_board(curses.LINES-2, curses.COLS-2)
    #initial = edgepad_board(glider, top=10, bottom=10, left=10, right=10)
    height = len(initial) + 2
    width = len(initial[0]) + 2
    pad = curses.newwin(height, width)

    game = game_of_life_wraparound(initial)
    for move in game:
        char = pad.getch()      # any keypress quits
        if char != curses.ERR:
            return

        pad.erase()
        pad.box()
        display_curses(pad, move, 1, 1)  # offsets leave room for box
        pad.refresh()

if __name__ == "__main__":
    # run(glider)
    curses.wrapper(run_curses)
