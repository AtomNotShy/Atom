import json
import random

import numpy as np
from copy import deepcopy


search_depth = 2
branch_factor = 25


class Board:
    def __init__(self, n=5):
        self.size = n
        self.board = np.zeros((n, n))
        self.prev_board = np.zeros((n, n))
        self.side = None
        self.n_move = 0
        self.max_move = 12

    def loadBoard(self):
        self.readInput()
        return self

    def readInput(self):
        with open('./input.txt') as f:
            lines = f.readlines()
            self.side = int(lines[0])
            self.prev_board = np.array([[int(x) for x in line.rstrip('\n')] for line in lines[1: self.size + 1]])
            self.board = np.array(
                [[int(x) for x in line.rstrip('\n')] for line in lines[self.size + 1: 2 * self.size + 1]])

    def copy(self):  # from host
        return deepcopy(self)

    def update_board(self, new_board):  # from host
        self.board = new_board

    def is_valid(self, i, j, side):  # from host
        if (not 0 <= i < self.size) or (not 0 <= j < self.size):
            return False

        if self.board[i][j] != 0:
            return False
        test_game = self.copy()
        test_board = test_game.board

        # Check if the place has liberty
        test_board[i][j] = side
        test_game.update_board(test_board)
        if test_game.check_liberty(i, j):
            return True

        test_game.remove_dead_stones(3 - side)
        if not test_game.check_liberty(i, j):
            return False
        else:
            if self.is_same_board(self.prev_board, test_game.board):
                return False
        return True

    def move_a_step(self, i, j, side):  # from host
        if (not 0 <= i < self.size) or (not 0 <= j < self.size) or self.board[i][j] != 0:
            raise Exception
        self.board[i][j] = side
        self.remove_dead_stones(3 - side)

    def neighbors(self, i, j):  # from host
        for direction in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            temp_i, temp_j = i + direction[0], j + direction[1]
            if 0 <= temp_i < self.size and 0 <= temp_j < self.size:
                yield [temp_i, temp_j]

    def check_singe_liberty(self, i, j):
        liberty = 0
        for neighbor in self.neighbors(i, j):
            if self.board[neighbor[0]][neighbor[1]] == 0:
                liberty += 1
        return liberty

    def check_liberty(self, i, j):
        allies = self.find_ally(i, j)
        liberty = 0
        for ally in allies:
            liberty += self.check_singe_liberty(ally[0], ally[1])
        return liberty

    def check_block_liberty(self, stones):
        res = 0
        seen = dict()
        for stone in stones:
            for neighbor in self.neighbors(stone[0], stone[1]):
                if str(neighbor) not in seen.keys():
                    seen[str(neighbor)] = 1
                    if self.board[neighbor[0]][neighbor[1]] == 0:
                        res += 1
        return res

    def find_ally(self, i, j):  # from host
        queue = [[i, j]]
        res = []
        while queue:
            cur = queue.pop(0)
            res.append(cur)
            neighbors = self.neighbors(cur[0], cur[1])
            for neighbor in neighbors:
                if self.board[neighbor[0]][neighbor[1]] == self.board[i][j] \
                        and [neighbor[0], neighbor[1]] not in queue \
                        and [neighbor[0], neighbor[1]] not in res:
                    queue.append(neighbor)
        return res

    def remove_dead_stones(self, side):  # from host
        dead_stones = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == side:
                    block = self.find_ally(i, j)
                    if self.check_block_liberty(block) == 0:
                        self.remove_stone_in_block(block)
                        dead_stones += block
        return dead_stones

    def remove_single_stone(self, i, j):
        self.board[i][j] = 0

    def remove_stone_in_block(self, stones):
        for stone in stones:
            self.remove_single_stone(stone[0], stone[1])

    def is_same_board(self, board1, board2):
        for i in range(self.size):
            for j in range(self.size):
                if board1[i][j] != board2[i][j]:
                    return False
        return True

    def evaluate_liberty2(self):  # from host
        res1, res2 = 0, 0
        temp = deepcopy(self)
        for i in range(0, temp.size):
            for j in range(0, temp.size):
                if temp.board[i][j] not in [1, 2]:
                    continue
                allys = temp.find_ally(i, j)
                res = temp.check_block_liberty(allys)
                if temp.board[i][j] == 1:
                    res1 += res
                else:
                    res2 += res
        return res1, res2

    def evaluate_liberty(self):
        visited = dict()
        res1, res2 = 0, 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] not in [1, 2] or str([i, j]) in visited:
                    continue
                allies = self.find_ally(i, j)
                liberty = self.cal_block_liberty(allies)
                if self.board[i][j] == 1:
                    res1 += liberty
                else:
                    res2 += liberty

                for ally in allies:
                    visited[str(ally)] = -1
        return res1, res2

    def evaluate_score(self):  # from host
        res1, res2 = 0, 0
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.board[i][j] == 1:
                    res1 += 1
                elif self.board[i][j] == 2:
                    res2 += 1
        return res1, res2

    def evaluate_location(self):
        res1, res2 = 0, 0
        ls = [1, 2, 1, 2, 1]
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 1:
                    res1 += (ls[i] + ls[j]) / 2
                else:
                    res2 += (ls[i] + ls[j]) / 2
        return res1, res2

    def cal_block_liberty(self, stones):
        res = 0
        seen = dict()
        for stone in stones:
            for neighbor in self.neighbors(stone[0], stone[1]):
                if self.board[neighbor[0]][neighbor[1]] == 0 and str(neighbor) not in seen.keys():
                    res += 1
                    seen[str(neighbor)] = 1
        return res

    def game_end(self, action="PASS"):  # from host
        # Case 1: max move reached
        if self.n_move >= self.max_move:
            return True
        # Case 2: two players all pass the move.
        if self.is_same_board(self.prev_board, self.board) and action == "PASS":
            return True
        return False

    def visualize_board(self):  # from host
        board = self.board
        print('-' * self.size * 2)
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == 0:
                    print('-', end=' ')
                elif board[i][j] == 1:
                    print('X', end=' ')
                else:
                    print('O', end=' ')
            print()
        print('-' * len(board) * 2)


class BasePlayer:
    def __init__(self):
        self.type = 'base'
        self.board = Board(5)

    def play_one_step(self):
        self.board = Board(5).loadBoard()
        action = self.getInput()
        self.board.n_move += 1
        Board.visualize_board(self.board)
        self.writeOutput(action)

    def writeOutput(self, move):  # from host
        if move != "PASS":
            res = str(move[0]) + ',' + str(move[1])
        else:
            res = "PASS"

        with open('./output.txt', 'w') as f:
            f.write(res)

    def getInput(self):
        raise NotImplementedError

    def evaluate(self, cur_board, side):
        score = cur_board.evaluate_score()
        liberty = cur_board.evaluate_liberty()
        liberty2 = cur_board.evaluate_liberty2()   # + (location_score[0] - location_score[1]) + (liberty2[0] - liberty2[1])
        location_score = cur_board.evaluate_location()
        if side == 1:
            return (score[0] - score[1]) + 0.5*(liberty2[0] - liberty2[1])
        else:
            return -((score[0] - score[1]) + 0.5*(liberty2[0] - liberty2[1]))

    def find_valid_locations(self, board, side):
        res = []
        for i in range(board.size):
            for j in range(board.size):
                if board.is_valid(i, j, side):
                    res.append([i, j])
        return res


class ABPPlayer(BasePlayer):
    def __init__(self):
        super(ABPPlayer, self).__init__()
        self.type = 'alpha beta pruning search'
        self.search_depth = search_depth
        self.branch_factor = branch_factor

    def getInput(self):
        action = self.abp_search(self.board, self.board.side)
        if not action:
            return "PASS"
        else:
            return action

    def find_locations(self, board, side):
        locations = self.find_valid_locations(board, side)
        np.random.shuffle(locations)
        if len(locations) > self.branch_factor:
            locations = locations[:self.branch_factor]
        return locations

    def abp_search(self, board: Board, side):
        res = self.maxEval(board, side, float('-inf'), float('inf'), self.search_depth)[1]
        return res

    def maxEval(self, board, side, a, b, d):
        if d == 0:
            if side == 1:
                temp = None
            else:
                temp = -self.evaluate(board, side)

            return self.evaluate(board, side), temp

        locations = self.find_locations(board, side)
        score = float('-inf')
        act = None

        for location in locations:
            temp_board = board.copy()
            temp_board.move_a_step(location[0], location[1], side)
            old_score = score
            score = max(score, self.minEval(temp_board, 3 - side, a, b, d - 1))
            if score != old_score:
                act = location
            if score >= b:
                return score, act
            a = max(a, score)
        return score, act

    def minEval(self, board, side, a, b, d):
        if d == 0 or board.game_end():
            return self.evaluate(board, side) if side == 1 else -self.evaluate(board, side)

        locations = self.find_locations(board, side)
        score = float('inf')

        for location in locations:
            temp_board = board.copy()
            temp_board.move_a_step(location[0], location[1], side)

            score = min(score, self.maxEval(temp_board, 3 - side, a, b, d - 1)[0])
            if score <= a:
                return score
            b = min(b, score)
        return score


if __name__ == '__main__':
    player = ABPPlayer()
    player.play_one_step()

