import uuid
SIZE, MARGIN, N = 540, 23, 15
GRID = (SIZE - 2 * MARGIN) / (N-1)

def pos_pixel2map(x, y):
    j = round((x - MARGIN) / GRID)
    i = round((y - MARGIN) / GRID)
    return i, j

def create_mapping():
    return {(i, j): (MARGIN + j*GRID, MARGIN + i*GRID) for i in range(N) for j in range(N)}

def create_pattern_dict():
    d = {}
    for x in [-1, 1]:
        y = -x
        d[(x,x,x,x)] = 1000000 * x # Thắng 4
        d[(0,x,x,x,0)] = 100000 * x # 3 thoáng 2 đầu
        d[(0,x,x,x,y)] = 10000 * x; d[(y,x,x,x,0)] = 10000 * x
        d[(0,x,x,0)] = 1000 * x; d[(0,x,0,x,0)] = 1000 * x
    return d

def init_zobrist():
    return [[[uuid.uuid4().int for _ in range(2)] for j in range(N)] for i in range(N)]

def update_TTable(table, hash, score, depth):
    table[hash] = [score, depth]