import pickle
import sys

# import numpy as np
import random
import math

import pygame as pygame

import Board
import copy
import time
import gzip
# import matplotlib.pyplot as plt

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


class TreeNode:
    def __init__(self, state, parent, turn, level):
        self.state = state
        self.score = 0
        self.visits = 0
        self.parent = parent
        self.children = []
        self.turn = turn
        self.Poss_Child = GetNeighbourMoves(state, level)
        self.level = level


Rows = 6
Cols = 5
CC = 2


# This function check if the game is draw
# it returns False if anyone player has won
# and if the game can be continued and none won
# else it returns true
def checkdraw(board):
    count = 0
    if checkwin(board) == 0 or checkwin(board) == 1:
        return False
    else:
        for c in range(len(board[0])):
            if board[0][c] != 2:
                count = count + 1
        if count == Cols:
            return True
    return False


# This checks which player has won the game
# returns 0 if player 0 has won or 1 if player 1 has won
# returns 2 if none has won i.e. either draw or game can be continued
def checkwin(board):
    for r in range(Rows):
        for c in range(Cols - 3):
            if board[r][c] == 0 and board[r][c + 1] == 0 and board[r][c + 2] == 0 and board[r][c + 3] == 0:
                return 0
            if board[r][c] == 1 and board[r][c + 1] == 1 and board[r][c + 2] == 1 and board[r][c + 3] == 1:
                return 1

    for r in range(Rows - 3):
        for c in range(Cols):
            if board[r][c] == 0 and board[r + 1][c] == 0 and board[r + 2][c] == 0 and board[r + 3][c] == 0:
                return 0
            if board[r][c] == 1 and board[r + 1][c] == 1 and board[r + 2][c] == 1 and board[r + 3][c] == 1:
                return 1

    for r in range(Rows - 3):
        for c in range(Cols - 3):
            if board[r][c] == 0 and board[r + 1][c + 1] == 0 and board[r + 2][c + 2] == 0 and board[r + 3][c + 3] == 0:
                return 0
            if board[r][c] == 1 and board[r + 1][c + 1] == 1 and board[r + 2][c + 2] == 1 and board[r + 3][c + 3] == 1:
                return 1

    for r in range(3, Rows):
        for c in range(Cols - 3):
            if board[r][c] == 0 and board[r - 1][c + 1] == 0 and board[r - 2][c + 2] == 0 and board[r - 3][c + 3] == 0:
                return 0
            if board[r][c] == 1 and board[r - 1][c + 1] == 1 and board[r - 2][c + 2] == 1 and board[r - 3][c + 3] == 1:
                return 1
    return 2


# This is a very important function and it returns the
# possible children possible for a parent node i.e. if a board has state A
# what are the next state possible
def GetNeighbourMoves(parent_node, level):
    child_nodes = []
    for i in range(Cols):
        board_cpy = copy.deepcopy(parent_node)
        if board_cpy[0][i] == 2:
            for j in range(Rows):
                if board_cpy[Rows-j-1][i] == 2:
                    board_cpy[Rows-j-1][i] = level ^ 1
                    child_nodes.append(board_cpy)
                    break
    return child_nodes


# Function for selection in MCTS
# it selects the child which has the best uct score and returns it
# or selects the child which has not been visited even once
def selection(parent_node):
    n = len(parent_node.children)
    # if n == Cols:
    #     return parent_node
    # else:
    best_score = -100
    best_child = parent_node
    for i in range(n):
        if parent_node.children[i].visits == 0:
            return parent_node.children[i]
        else:
            score = parent_node.children[i].score / parent_node.children[i].visits
            score += math.sqrt(CC * math.log(parent_node.visits) / parent_node.children[i].visits)
            if score > best_score:
                best_score = score
                best_child = parent_node.children[i]
    return best_child


def expansion(parent_node):
    next_node = random.choice(parent_node.Poss_Child)
    nodes = parent_node.Poss_Child
    index = nodes.index(next_node)
    nodes.pop(index)
    parent_node.Poss_Child = nodes
    # for i in range(len(parent_node.Poss_Child)):
    #     if parent_node.Poss_Child[i] != next_node:
    #         nodes.append(parent_node.Poss_Child[i])
    # parent_node.Poss_Child = nodes
    child = TreeNode(next_node, parent_node, 1 ^ parent_node.turn, parent_node.level ^ 1)
    parent_node.children.append(child)
    return child


def simulation(board, level):
    # printstate(board)
    # i = 1
    while True:
        # printstate(board)
        moves = GetNeighbourMoves(board, level)
        # if i == 5:
        #     printstate(moves[0])
        #     printstate(moves[1])
        #     printstate(moves[2])
        #     printstate(moves[3])
        #     printstate(moves[4])
        # i += 1
        if not moves:
            return checkwin(board)
        board = random.choice(moves)
        if (checkwin(board) == 2 and checkdraw(board)) or checkwin(board) == 1 or checkwin(board) == 0:
            break
        level = level ^ 1
    return checkwin(board)


def update(result, parent_node):
    while parent_node != None:
        # if result == parent_node.level:
        #     parent_node.score = parent_node + 1
        if result != 2:
            parent_node.score = (-1)**(parent_node.level+result) + parent_node.score
        parent_node.visits = parent_node.visits + 1
        parent_node = parent_node.parent


def printstate(board):
    lol = board


def islegal(board,col):
    if board[0][col] == 2:
        return True
    return False


# This is a function to simulate the game for human player
#     here we take the input from the user and play it on the board
def human_player(current_node, board, turn, level, col):
    printstate(board)
    board_cpy = copy.deepcopy(board)
    printstate(board_cpy)
    i = 0
    while board_cpy[i][col] == 2 and i < Rows-1:
        i += 1
    if board_cpy[i][col] != 2:
        i -= 1
    board_cpy[i][col] = turn ^ 1
    board = board_cpy
    printstate(board)
    return TreeNode(board, current_node, turn ^ 1, level ^ 1)


def mcts_n(parent_node, n):
    initial_node = copy.deepcopy(parent_node)
    while n > 0 and checkwin(parent_node.state) == 2 and not checkdraw(parent_node.state):
        if parent_node.Poss_Child and random.uniform(0, 1) >= 0:
            parent_node = expansion(parent_node)
            result = simulation(parent_node.state, parent_node.level)
            update(result, parent_node)
            parent_node = initial_node
            n = n - 1
        else:
            parent_node = selection(parent_node)

    parent_node = initial_node
    lists = []
    parent_node = initial_node
    for i in parent_node.children:
        if checkwin(i.state) == parent_node.turn:
            return i
        if not lists:
            lists.append(i)
        else:
            if lists[0].visits < i.visits:
                lists = [i]
            elif lists[0].visits == i.visits:
                lists.append(i)
    #print(lists[0].state)
    if lists:
        child = lists[0]
    else:
        child = TreeNode(random.choice(GetNeighbourMoves(initial_node.state, initial_node.level)), initial_node, initial_node.turn ^ 1, initial_node.level ^ 1)
    maxscore = -10
    for i in lists:
        if i.score > maxscore:
            child = i
            maxscore = i.score
    return child


def MCTS_vs_MCTS():
    turn = 0
    count = 0
    draw = 0
    winner2 = 0
    num_games = 10
    in_time = time.time()
    for _ in range(num_games):
        print(_)
        board = Board.create_board()
        current_node = TreeNode(board, None, 0, 0)
        current_state = current_node.state
        lastmove = 0
        while checkwin(current_state) == 2 and not checkdraw(current_state):
            if turn == 0:
                print("__MCTS-200__")
                current_node = mcts_n(current_node, 2000)
                # current_node = human_player(current_node, current_state, turn, current_node.level)
                current_state = current_node.state
                lastmove = 1
            else:
                print("__MCTS-40__")
                current_node = mcts_n(current_node, 6)
                current_state = current_node.state
                lastmove = 0
            turn = turn ^ 1
        print("GAME-CHANGE")
        if checkdraw(current_state):
            draw += 1
        else:
            if lastmove == 0 and checkwin(current_state) != 2:
                count += 1
            else:
                winner2 += 1
    print(time.time()-in_time)
    print("MCT40 = ", count, "Draw = ", draw, "MCT200 = ", winner2)



class qlnode():
    def __init__(self, qtable, alpha, gamma, epsilon):
        self.epsilon = epsilon
        self.q_table = qtable
        self.tot_reward = 0
        self.alpha = alpha
        self.gamma = gamma


gamma = 0.7
epsilon = 0.3
alpha = 0.8


def q_play(parent_node):
    next_child = GetNeighbourMoves(parent_node.state, parent_node.level)
    exploit_or_not = random.uniform(0, 1)
    last_state = parent_node.state
    last_state_action = str(last_state)
    #next_node = parent_node
    if not next_child:
        return None, None
    else:
        # print(epsilon)
        if exploit_or_not < epsilon:
            i = random.choice(next_child)
            key = str(parent_node.state) + str(i)
            if key not in qtable:
                qtable[key] = 0
            next_node = TreeNode(i, parent_node, parent_node.turn ^ 1, parent_node.level ^ 1)
        else:
            score_max = -10000000
            for i in next_child:
                key = str(parent_node.state) + str(i)
                if key not in qtable:
                    qtable[key] = 0
                if key in qtable and qtable[key] > score_max:
                    score_max = qtable[key]
                    last_state_action = key
                    last_state = i
            next_node = TreeNode(last_state, parent_node, parent_node.turn ^ 1, parent_node.level ^ 1)
        return next_node, last_state_action


qtable = {}


def q_update(parent_node, last_state_action):
    score_max = -10000000
    best_state = parent_node.state
    next_child = GetNeighbourMoves(parent_node.state, parent_node.level)
    reward = 0
    flag = True
    for i in next_child:
        key = str(parent_node.state) + str(i)
        if key not in qtable:
            qtable[key] = 0
        if score_max < qtable[key]:
            best_state = i
            score_max = qtable[key]
        if checkwin(i) == parent_node.level ^ 1:
            reward = 100
        elif checkwin(i) == parent_node.level:
            reward = -100
    draw_val = checkdraw(best_state)
    win_val = checkwin(best_state)
    if flag:
        if not draw_val:
            reward = -1
        elif draw_val:
            reward = -5
        elif win_val == parent_node.level ^ 1:
            reward = 100
        elif win_val == parent_node.level:
            reward = -100
    if last_state_action in qtable:
        qtable[last_state_action] += alpha * (reward + gamma*score_max - qtable[last_state_action])
    else:
        qtable[last_state_action] = 0
    return reward


def game_driver(screen, SQAIZE, width, RADIUS):
    turn = 0
    count = 0
    draw = 0
    winner2 = 0
    num_games = 1
    in_time = time.time()
    qtable = pickle.load(gzip.open("C:\\Users\\agraw\\PycharmProjects\\AI-Assignment2\\20180827_final_5.dat.gz", "rb"))
    board = Board.create_board()
    current_node = TreeNode(board, None, 0, 0)
    current_state = current_node.state
    lastmove = 0
    while checkwin(current_state) == 2 and not checkdraw(current_state):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQAIZE))
                px = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (px, int(SQAIZE/2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (px, int(SQAIZE/2)), RADIUS)
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if turn == 0:
                    px = event.pos[0]
                    col = int(math.floor(px/SQAIZE))
                    current_node = human_player(current_node, current_state, turn, current_node.level, col)
                    current_state = current_node.state
                    lastmove = 1
                else:
                    px = event.pos[0]
                    col = int(math.floor(px / SQAIZE))
                    current_node = mcts_n(current_node, 200)
                    current_state = current_node.state
                    printstate(current_state)
                    lastmove = 0
                turn = turn ^ 1
                draw_board(current_state, screen, SQAIZE, RADIUS)
    pygame.time.wait(3000)


def draw_board(board, screen, SQAIZE, RADIUS):
    for c in range(Cols):
        for r in range(Rows):
            pygame.draw.rect(screen, BLUE, (c*SQAIZE, r*SQAIZE+SQAIZE, SQAIZE, SQAIZE))
            if board[r][c] == 2:
                pygame.draw.circle(screen, BLACK, (int(c*SQAIZE+SQAIZE/2), int(r*SQAIZE+SQAIZE+SQAIZE/2)), RADIUS)
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQAIZE+SQAIZE/2), int(r*SQAIZE+SQAIZE+SQAIZE/2)), RADIUS)
            if board[r][c] == 0:
                pygame.draw.circle(screen, YELLOW, (int(c*SQAIZE+SQAIZE/2), int(r*SQAIZE+SQAIZE+SQAIZE/2)), RADIUS)
    pygame.display.update()


def main():
    pygame.init()
    SQAIZE = 100
    width = Cols * SQAIZE
    height = (Rows + 1) * SQAIZE
    size = (width, height)
    RADIUS = int(SQAIZE/2-3)
    screen = pygame.display.set_mode(size)
    pygame.display.update()
    game_driver(screen, SQAIZE, width, RADIUS)


if __name__ == '__main__':
    main()
