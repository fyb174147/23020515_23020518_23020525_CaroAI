import math
import sys

import source.utils as utils

sys.setrecursionlimit(10000)

N = 15
WIN_LENGTH = 4
WIN_SCORE = 10_000_000


class GomokuAI:
    def __init__(self, depth=3):
        self.depth = depth
        self.boardMap = [[0 for _ in range(N)] for _ in range(N)]
        self.currentI, self.currentJ = -1, -1
        self.nextBound = {}
        self.boardValue = 0
        self.turn = -1
        self.lastPlayed = 0
        self.emptyCells = N * N
        self.patternDict = utils.create_pattern_dict()
        self.zobristTable = utils.init_zobrist()
        self.rollingHash = 0
        self.TTable = {}
        self.ai_mode = "alphabeta"
        self.nodes_visited = 0
        self.bestI = -1
        self.bestJ = -1
        self.bestValue = 0
        self.last_search_time = 0.0

    def _hash_index(self, state):
        return 0 if state == 1 else 1

    def setState(self, i, j, state):
        """Place a real move on the board."""
        if not self.isValid(i, j):
            return False
        self.boardMap[i][j] = state
        self.rollingHash ^= self.zobristTable[i][j][self._hash_index(state)]
        self.lastPlayed = state
        self.currentI, self.currentJ = i, j
        self.emptyCells -= 1
        return True

    def isValid(self, i, j, state=True):
        if i < 0 or i >= N or j < 0 or j >= N:
            return False
        if state:
            return self.boardMap[i][j] == 0
        return True

    def isFour(self, i, j, state):
        """Check the assignment rule: 4 consecutive stones win."""
        if i < 0 or j < 0 or state == 0:
            return False
        directions = [
            ((-1, 0), (1, 0)),
            ((0, -1), (0, 1)),
            ((-1, 1), (1, -1)),
            ((-1, -1), (1, 1)),
        ]
        for axis in directions:
            count = 1
            for xdir, ydir in axis:
                for step in range(1, WIN_LENGTH):
                    ni, nj = i + ydir * step, j + xdir * step
                    if 0 <= ni < N and 0 <= nj < N and self.boardMap[ni][nj] == state:
                        count += 1
                    else:
                        break
            if count >= WIN_LENGTH:
                return True
        return False

    def checkResult(self):
        if self.currentI == -1:
            return 0 if self.emptyCells <= 0 else None
        if self.isFour(self.currentI, self.currentJ, self.lastPlayed):
            return self.lastPlayed
        return 0 if self.emptyCells <= 0 else None

    def childNodes(self, bound):
        if not bound:
            center = N // 2
            if self.boardMap[center][center] == 0:
                yield (center, center)
                return
            for i in range(N):
                for j in range(N):
                    if self.boardMap[i][j] == 0:
                        yield (i, j)
            return

        center = (N - 1) / 2

        def sort_key(item):
            (i, j), score = item
            distance = abs(i - center) + abs(j - center)
            return (score, -distance)

        for pos, _ in sorted(bound.items(), key=sort_key, reverse=True):
            i, j = pos
            if self.isValid(i, j):
                yield pos

    def updateBound(self, new_i, new_j, bound):
        played = (new_i, new_j)
        bound.pop(played, None)
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, 1), (1, -1), (-1, -1), (1, 1),
        ]
        for dx, dy in directions:
            ni, nj = new_i + dy, new_j + dx
            if 0 <= ni < N and 0 <= nj < N and self.boardMap[ni][nj] == 0:
                bound.setdefault((ni, nj), 0)

    def _terminal_score(self, depth):
        winner = self.checkResult()
        if winner == 1:
            return WIN_SCORE + depth
        if winner == -1:
            return -WIN_SCORE - depth
        if winner == 0:
            return 0
        return None

    def _play_temp(self, i, j, turn):
        old = (self.currentI, self.currentJ, self.lastPlayed, self.emptyCells)
        self.boardMap[i][j] = turn
        self.currentI, self.currentJ, self.lastPlayed = i, j, turn
        self.emptyCells -= 1
        self.rollingHash ^= self.zobristTable[i][j][self._hash_index(turn)]
        return old

    def _undo_temp(self, i, j, turn, old):
        self.boardMap[i][j] = 0
        self.currentI, self.currentJ, self.lastPlayed, self.emptyCells = old
        self.rollingHash ^= self.zobristTable[i][j][self._hash_index(turn)]

    def alphaBetaPruning(self, depth, board_value, bound, alpha, beta, maximizingPlayer):
        self.nodes_visited += 1
        terminal = self._terminal_score(depth)
        if terminal is not None:
            return terminal
        if depth <= 0:
            return board_value

        table_key = (self.rollingHash, depth, maximizingPlayer)
        cached = self.TTable.get(table_key)
        if cached is not None:
            return cached

        root = depth == self.depth
        if root:
            self.bestI, self.bestJ = -1, -1

        res_val = -math.inf if maximizingPlayer else math.inf
        has_child = False

        for i, j in self.childNodes(bound):
            has_child = True
            turn = 1 if maximizingPlayer else -1
            new_bound = dict(bound)
            new_val = self.evaluate(i, j, board_value, turn, new_bound)
            old = self._play_temp(i, j, turn)
            self.updateBound(i, j, new_bound)

            child_val = self.alphaBetaPruning(
                depth - 1, new_val, new_bound, alpha, beta, not maximizingPlayer
            )

            self._undo_temp(i, j, turn, old)

            if maximizingPlayer:
                if child_val > res_val:
                    res_val = child_val
                    if root:
                        self.bestI, self.bestJ = i, j
                        self.bestValue = child_val
                        self.boardValue = new_val
                        self.nextBound = new_bound
                alpha = max(alpha, res_val)
            else:
                if child_val < res_val:
                    res_val = child_val
                    if root:
                        self.bestI, self.bestJ = i, j
                        self.bestValue = child_val
                        self.boardValue = new_val
                        self.nextBound = new_bound
                beta = min(beta, res_val)

            if beta <= alpha:
                break

        if not has_child:
            res_val = 0

        self.TTable[table_key] = res_val
        if root and self.bestI != -1:
            self.currentI, self.currentJ = self.bestI, self.bestJ
        return res_val

    def minimax(self, depth, board_value, bound, maximizingPlayer):
        self.nodes_visited += 1
        terminal = self._terminal_score(depth)
        if terminal is not None:
            return terminal
        if depth <= 0:
            return board_value

        root = depth == self.depth
        if root:
            self.bestI, self.bestJ = -1, -1

        res_val = -math.inf if maximizingPlayer else math.inf
        has_child = False

        for i, j in self.childNodes(bound):
            has_child = True
            turn = 1 if maximizingPlayer else -1
            new_bound = dict(bound)
            new_val = self.evaluate(i, j, board_value, turn, new_bound)
            old = self._play_temp(i, j, turn)
            self.updateBound(i, j, new_bound)

            child_val = self.minimax(depth - 1, new_val, new_bound, not maximizingPlayer)

            self._undo_temp(i, j, turn, old)

            if maximizingPlayer:
                if child_val > res_val:
                    res_val = child_val
                    if root:
                        self.bestI, self.bestJ = i, j
                        self.bestValue = child_val
                        self.boardValue = new_val
                        self.nextBound = new_bound
            else:
                if child_val < res_val:
                    res_val = child_val
                    if root:
                        self.bestI, self.bestJ = i, j
                        self.bestValue = child_val
                        self.boardValue = new_val
                        self.nextBound = new_bound

        if not has_child:
            res_val = 0

        if root and self.bestI != -1:
            self.currentI, self.currentJ = self.bestI, self.bestJ
        return res_val

    def firstMove(self, state=1):
        self.boardValue = self.evaluate(N // 2, N // 2, self.boardValue, state, self.nextBound)
        self.setState(N // 2, N // 2, state)
        self.updateBound(N // 2, N // 2, self.nextBound)

    def evaluate(self, new_i, new_j, board_value, turn, bound):
        """Incrementally score the board from player 1's perspective."""
        v_before = 0
        v_after = 0
        for pattern, score in self.patternDict.items():
            v_before += self.countPattern(new_i, new_j, pattern, abs(score), bound, -1) * score
            self.boardMap[new_i][new_j] = turn
            v_after += self.countPattern(new_i, new_j, pattern, abs(score), bound, 1) * score
            self.boardMap[new_i][new_j] = 0
        return board_value + v_after - v_before

    def countPattern(self, i_0, j_0, pattern, score, bound, flag):
        directions = [(1, 0), (1, 1), (0, 1), (-1, 1)]
        length = len(pattern)
        count = 0
        for direction in directions:
            if direction[0] * direction[1] == 0:
                steps_back = direction[0] * min(5, j_0) + direction[1] * min(5, i_0)
            elif direction[0] == 1:
                steps_back = min(5, j_0, i_0)
            else:
                steps_back = min(5, N - 1 - j_0, i_0)
            i_start = i_0 - steps_back * direction[1]
            j_start = j_0 - steps_back * direction[0]
            z = 0
            while z <= steps_back:
                i_new = i_start + z * direction[1]
                j_new = j_start + z * direction[0]
                idx = 0
                rem = []
                while (
                    idx < length
                    and 0 <= i_new < N
                    and 0 <= j_new < N
                    and self.boardMap[i_new][j_new] == pattern[idx]
                ):
                    if self.boardMap[i_new][j_new] == 0:
                        rem.append((i_new, j_new))
                    i_new += direction[1]
                    j_new += direction[0]
                    idx += 1
                if idx == length:
                    count += 1
                    for pos in rem:
                        bound[pos] = bound.get(pos, 0) + flag * score
                    z += idx
                else:
                    z += 1
        return count

    def getWinner(self):
        res = self.checkResult()
        if res == 1:
            return "Black"
        if res == -1:
            return "White"
        return "Tie"
