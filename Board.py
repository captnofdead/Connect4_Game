import numpy as np
import random
import math
import copy
Rows = 5
Cols = 6


def create_board(n=5, m=6):
    Rows = n
    Cols = m
    board = []
    board_row = []
    for r in range(Rows):
        board_row.append(2)
    for c in range(Cols):
        board.append(copy.deepcopy(board_row))
    return board


def final_move(board, move):
    for r in range(Rows):
        for c in range(Cols-3):
            if board[r][c] == move and board[r][c+1] == move and board[r][c+2] == move and board[r][c+3] == move:
                return True

    for r in range(Rows-3):
        for c in range(Cols):
            if board[r][c] == move and board[r+1][c] == move and board[r+2][c] == move and board[r+3][c] == move:
                return True

    for r in range(Rows-3):
        for c in range(Cols-3):
            if board[r][c] == move and board[r+1][c+1] == move and board[r+2][c+2] == move and board[r+3][c+3] == move:
                return True

    for r in range(3, Rows):
        for c in range(Cols-3):
            if board[r][c] == move and board[r-1][c+1] == move and board[r-2][c+2] == move and board[r-3][c+3] == move:
                return True

    count = 0

    for c in range(Cols):
        if board[0][c] != 0:
            count = count + 1
    if count == Cols:
        return 3

    return False


def get_turn(turn):
    if turn == 0:
        turn = turn + 1
    else:
        turn = turn + 1
        turn = turn % 2
    return turn


def valid_move(board, turn):
    if board[0][turn] == 0:
        return True
    return False


def valid_moves(board):
    moves = []
    for c in range(Cols):
        if board[0][c] == 0:
            moves.append(c)
    return moves


def get_next_open_row(board, col):
    for r in range(Rows):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(board)
    
