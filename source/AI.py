import math
import sys
import source.utils as utils

sys.setrecursionlimit(2000)
N = 15 # board size 15x15

class GomokuAI():
    def __init__(self, depth=3):
        self.depth = depth
        self.boardMap = [[0 for j in range(N)] for i in range(N)]
        self.currentI, self.currentJ = -1, -1
        self.nextBound = {}
        self.boardValue = 0 
        self.turn = 0 
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

    def setState(self, i, j, state):
        """Đặt quân cờ và cập nhật trạng thái mới nhất"""
        self.boardMap[i][j] = state
        self.lastPlayed = state
        self.currentI, self.currentJ = i, j
        self.emptyCells -= 1

    def isValid(self, i, j, state=True):
        """Kiểm tra nước đi có hợp lệ không (trong bàn cờ và ô trống)"""
        if i < 0 or i >= N or j < 0 or j >= N:
            return False
        if state:
            return self.boardMap[i][j] == 0
        return True

    def isFour(self, i, j, state):
        """Kiểm tra luật 4 quân thắng [cite: 16, 25]"""
        directions = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, 1), (1, -1)], [(-1, -1), (1, 1)]]
        for axis in directions:
            count = 1
            for (xdir, ydir) in axis:
                for step in range(1, 5):
                    ny, nx = i + ydir*step, j + xdir*step
                    if 0 <= ny < N and 0 <= nx < N and self.boardMap[ny][nx] == state:
                        count += 1
                    else: break
            if count >= 4: return True
        return False

    def checkResult(self):
        """Kiểm tra trạng thái kết thúc (Thắng/Thua/Hòa) [cite: 18, 134, 157]"""
        if self.currentI == -1: return None
        if self.isFour(self.currentI, self.currentJ, self.lastPlayed):
            return self.lastPlayed
        return 0 if self.emptyCells <= 0 else None

    def childNodes(self, bound):
        """Duyệt các nước đi tiềm năng theo thứ tự điểm số giảm dần [cite: 67]"""
        for pos in sorted(bound.items(), key=lambda el: el[1], reverse=True):
            yield pos[0]

    def updateBound(self, new_i, new_j, bound):
        """Cập nhật phạm vi tìm kiếm quanh các quân cờ đã đánh [cite: 64, 128]"""
        played = (new_i, new_j)
        if played in bound: bound.pop(played)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1), (-1, -1), (1, 1)]
        for dx, dy in directions:
            ni, nj = new_i + dy, new_j + dx
            if 0 <= ni < N and 0 <= nj < N and self.boardMap[ni][nj] == 0:
                if (ni, nj) not in bound: bound[(ni, nj)] = 0

    def alphaBetaPruning(self, depth, board_value, bound, alpha, beta, maximizingPlayer):
        self.nodes_visited += 1
        if depth <= 0 or self.checkResult() is not None:
            return board_value
        
        old_i, old_j, old_last = self.currentI, self.currentJ, self.lastPlayed
        res_val = -math.inf if maximizingPlayer else math.inf
        
        # Biến tạm để lưu nước đi tốt nhất tại tầng này
        best_move_at_depth = None 

        for i, j in self.childNodes(bound):
            new_bound = dict(bound)
            turn = 1 if maximizingPlayer else -1
            new_val = self.evaluate(i, j, board_value, turn, new_bound)
            
            self.boardMap[i][j] = turn
            self.currentI, self.currentJ, self.lastPlayed = i, j, turn
            self.updateBound(i, j, new_bound)

            eval = self.alphaBetaPruning(depth-1, new_val, new_bound, alpha, beta, not maximizingPlayer)

            self.boardMap[i][j] = 0
            self.currentI, self.currentJ, self.lastPlayed = old_i, old_j, old_last

            if maximizingPlayer:
                if eval > res_val:
                    res_val = eval
                    best_move_at_depth = (i, j)
                    if depth == self.depth:
                        # Chỉ cập nhật nước đi cuối cùng khi tìm thấy nước tốt nhất ở tầng gốc
                        self.bestI, self.bestJ = i, j 
                        self.boardValue, self.nextBound = eval, new_bound
                alpha = max(alpha, eval)
            else:
                if eval < res_val:
                    res_val = eval
                    best_move_at_depth = (i, j)
                beta = min(beta, eval)
            if beta <= alpha: break

        return res_val

    def minimax(self, depth, board_value, bound, maximizingPlayer):
        self.nodes_visited += 1
        # Điều kiện dừng: Thắng/Thua hoặc hết độ sâu
        if depth <= 0 or self.checkResult() is not None:
            return board_value 
        
        # Lưu trạng thái thực tế để khôi phục (Backtracking)
        old_i, old_j, old_last = self.currentI, self.currentJ, self.lastPlayed
        res_val = -math.inf if maximizingPlayer else math.inf

        for i, j in self.childNodes(bound):
            new_bound = dict(bound)
            turn = 1 if maximizingPlayer else -1
            new_val = self.evaluate(i, j, board_value, turn, new_bound)
            
            # GIẢ LẬP: Cập nhật tọa độ để checkResult() hoạt động
            self.boardMap[i][j] = turn
            self.currentI, self.currentJ, self.lastPlayed = i, j, turn
            self.updateBound(i, j, new_bound) 

            eval = self.minimax(depth - 1, new_val, new_bound, not maximizingPlayer)
            
            # HOÀN TÁC: Trả lại trạng thái cũ
            self.boardMap[i][j] = 0 
            self.currentI, self.currentJ, self.lastPlayed = old_i, old_j, old_last

            if maximizingPlayer:
                if eval > res_val:
                    res_val = eval
                    # CHỈ CẬP NHẬT KẾT QUẢ CUỐI CÙNG TẠI TẦNG GỐC
                    if depth == self.depth:
                        self.bestI, self.bestJ = i, j
                        self.boardValue, self.nextBound = eval, new_bound
            else:
                res_val = min(res_val, eval)
            
        return res_val

    def firstMove(self):
        """Máy đi trước vào giữa bàn cờ (7,7)"""
        self.setState(7, 7, 1)

    def evaluate(self, new_i, new_j, board_value, turn, bound):
        """Hàm đánh giá Heuristic [cite: 28, 137, 160]"""
        v_before = 0; v_after = 0
        for pattern, score in self.patternDict.items():
            v_before += self.countPattern(new_i, new_j, pattern, abs(score), bound, -1) * score
            self.boardMap[new_i][new_j] = turn
            v_after += self.countPattern(new_i, new_j, pattern, abs(score), bound, 1) * score
            self.boardMap[new_i][new_j] = 0
        return board_value + v_after - v_before

    def countPattern(self, i_0, j_0, pattern, score, bound, flag):
        directions = [(1, 0), (1, 1), (0, 1), (-1, 1)]; length = len(pattern); count = 0
        for dir in directions:
            if dir[0] * dir[1] == 0: steps_back = dir[0] * min(5, j_0) + dir[1] * min(5, i_0)
            elif dir[0] == 1: steps_back = min(5, j_0, i_0)
            else: steps_back = min(5, N-1-j_0, i_0)
            i_start, j_start = i_0 - steps_back * dir[1], j_0 - steps_back * dir[0]
            z = 0
            while z <= steps_back:
                i_new, j_new, idx, rem = i_start + z*dir[1], j_start + z*dir[0], 0, []
                while idx < length and 0 <= i_new < N and 0 <= j_new < N and self.boardMap[i_new][j_new] == pattern[idx]:
                    if self.boardMap[i_new][j_new] == 0: rem.append((i_new, j_new))
                    i_new, j_new, idx = i_new + dir[1], j_new + dir[0], idx + 1
                if idx == length:
                    count += 1
                    for pos in rem:
                        bound[pos] = bound.get(pos, 0) + flag*score
                    z += idx
                else: z += 1
        return count
    
    def getWinner(self):
        """Trả về tên người thắng dựa trên kết quả kiểm tra"""
        res = self.checkResult()
        if res == 1:
            return 'Gomoku AI!'
        elif res == -1:
            return 'Human!'
        return 'Tie'