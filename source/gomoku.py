import math, time, source.utils as utils 

def ai_move(ai):
    start_time = time.time()
    ai.nodes_visited = 0
    if ai.ai_mode == "minimax":
        ai.minimax(ai.depth, ai.boardValue, ai.nextBound, True)
    else:
        ai.alphaBetaPruning(ai.depth, ai.boardValue, ai.nextBound, -math.inf, math.inf, True)
    
    # In thông số cho Level 3 [cite: 30, 56]
    print(f"[{ai.ai_mode.upper()}] Time: {time.time()-start_time:.3f}s | Nodes: {ai.nodes_visited}")
    return ai.bestI, ai.bestJ

def check_human_move(ai, pos):
    i, j = utils.pos_pixel2map(pos[0], pos[1])
    if ai.isValid(i, j):
        ai.boardValue = ai.evaluate(i, j, ai.boardValue, -1, ai.nextBound)
        ai.setState(i, j, -1)
        ai.updateBound(i, j, ai.nextBound)
        return i, j
    return None