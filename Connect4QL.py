#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pickle
import numpy as np
import random
import math
import Board
import copy
import time
import gzip
import matplotlib.pyplot as plt
import numpy as np
import random
import math
import copy
Rows = 5
Cols = 6



def create_board(n = Rows, m = Cols):
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
                if board_cpy[Rows - j - 1][i] == 2:
                    board_cpy[Rows - j - 1][i] = level ^ 1
                    child_nodes.append(board_cpy)
                    break
    return child_nodes


# Function for selection in MCTS
# it selects the child which has the best uct score and returns it
# or selects the child which has not been visited even once
def selection(parent_node):
    n = len(parent_node.children)
    best_score = -100
    best_child = parent_node
    for i in range(n):
        if parent_node.children[i].visits == 0:
            return parent_node.children[i]
        else:
            score = parent_node.children[i].score / parent_node.children[i].visits + math.sqrt(
                CC * math.log(parent_node.visits) / parent_node.children[i].visits)
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
            parent_node.score = (-1) ** (parent_node.level + result) + parent_node.score
        parent_node.visits = parent_node.visits + 1
        parent_node = parent_node.parent


def printstate(board):
    row = []
    for r in board:
        print(r)
    print("---------------")


def islegal(board, col):
    if board[0][col] == 2:
        return True
    return False


# This is a function to simulate the game for human player
#     here we take the input from the user and play it on the board
def human_player(current_node, board, turn, level):
    printstate(board)
    print("Please select your  next move 1 to 6")
    col = int(input())
    while not islegal(board, col):
        print("that column is filled please enter another")
        col = int(input())
    board_cpy = copy.deepcopy(board)
    i = 0
    while board_cpy[i][col] == 2 and i < Rows - 1:
        i += 1
    print(i)
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
    # print(lists[0].state)
    if lists:
        child = lists[0]
    else:
        child = TreeNode(random.choice(GetNeighbourMoves(initial_node.state, initial_node.level)), initial_node,
                         initial_node.turn ^ 1, initial_node.level ^ 1)
    maxscore = -10
    for i in lists:
        if i.score > maxscore:
            child = i
            maxscore = i.score
    return child


def parta(node):
    initial_node = copy.deepcopy(node)
    turn = 0
    count = 0
    draw = 0
    winner2 = 0
    num_games = 1
    in_time = time.time()
    for _ in range(num_games):
        print(_)
        current_node = initial_node
        current_state = current_node.state
        lastmove = 0
        while checkwin(current_state) == 2 and not checkdraw(current_state):
            if turn == 0:
                current_node = mcts_n(current_node, 200)
                # current_node = human_player(current_node, current_state, turn, current_node.level)
                current_state = current_node.state
                print("MCTS_200 Move")
                printstate(current_state)
                lastmove = 1
            else:
                current_node = mcts_n(current_node, 6)
                current_state = current_node.state
                print("MCTS_40 Move")
                printstate(current_state)
                lastmove = 0
            turn = turn ^ 1
        if checkdraw(current_state):
            draw += 1
        else:
            if lastmove == 0 and checkwin(current_state) != 2:
                count += 1
            else:
                winner2 += 1
    print(time.time() - in_time)
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
    # next_node = parent_node
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
        qtable[last_state_action] += alpha * (reward + gamma * score_max - qtable[last_state_action])
    else:
        qtable[last_state_action] = 0
    return reward


def trainer():
    qtable = pickle.load(gzip.open("C:\\Users\\agraw\\PycharmProjects\\AI-Assignment2\\20180827_final_4.dat.gz", "rb"))
    qtable = {}
    initial_time = time.time()
    n = 10000
    draw = 0
    qlearn = 0
    mcts = 0
    start_time = time.time()
    print("Start")
    reward_episode = [0] * n
    i = 0
    while n > 0:
        print(n)
        # print("_________________NEW EPISODE_______________")
        board = Board.create_board(Cols, Rows)
        # printstate(board)
        initial_node = TreeNode(board, None, 0, 0)
        curr_node = mcts_n(initial_node, 40)

        # print("STARTT")
        # print("MCTS")
        # printstate(curr_node.state)
        while True:
            if checkdraw(curr_node.state):
                draw += 1
                break
            elif checkwin(curr_node.state) == 1:
                mcts += 1
                break
            curr_node, last_state_action = q_play(curr_node)
            # print("Q Learning")
            # printstate(curr_node.state)
            if checkdraw(curr_node.state):
                draw += 1
                break
            elif checkwin(curr_node.state) == 0:
                qlearn += 1
                break
            elif checkwin(curr_node.state) == 1:
                mcts += 1
                break
            curr_node = mcts_n(curr_node, 40)
            # print("MCTS")
            # printstate(curr_node.state)
            reward_episode[i] += q_update(curr_node, last_state_action)
            # print(reward_episode[i])
        # print(reward_episode[i])
        i += 1
        # printstate(curr_node.state)
        n -= 1
    # print(len(qtable))
    # print(qtable)
    pickle.dump(qtable, gzip.open("C:\\Users\\agraw\\PycharmProjects\\AI-Assignment2\\20180827_final_4.dat.gz", "wb"),
                protocol=pickle.HIGHEST_PROTOCOL)
    print("MCTs = ", mcts, " Qlearn = ", qlearn, " Draw ", draw)
    # print(-start_time+time.time())
    # print(reward_episode[0])
    plt.plot(range(len(reward_episode)), reward_episode)
    plt.show()


def main():
    turn = 0
    count = 0
    draw = 0
    winner2 = 0
    num_games = 100
    in_time = time.time()
    board = create_board()
    current_node = TreeNode(board, None, 0, 0)
    current_state = current_node.state
    lastmove = 0
    print("Enter game mode as given below: ")
    print("1) MCTS_40 vs MCTS_200")
    print("2) MC_n vs Q-Learning")

    inp = int(input())
    if inp == 1:
        parta(current_node)
    elif inp == 2:
        print("Input the value of n")
        n = inp = int(input())
        current_node = q_play(current_node)
    else:
        print("INVALID INPUT")


if __name__ == '__main__':
    main()

