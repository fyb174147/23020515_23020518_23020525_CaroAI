import math
import time

import source.utils as utils


def ai_move(ai, state):
    start_time = time.time()
    ai.nodes_visited = 0
    ai.TTable = {}
    maximizing = state == 1

    if ai.ai_mode == "minimax":
        value = ai.minimax(ai.depth, ai.boardValue, ai.nextBound, maximizing)
    else:
        value = ai.alphaBetaPruning(
            ai.depth, ai.boardValue, ai.nextBound, -math.inf, math.inf, maximizing
        )

    ai.last_search_time = time.time() - start_time
    ai.bestValue = value
    print(
        f"[{ai.ai_mode.upper()}] Player: {state:+d} | "
        f"Move: ({ai.bestI}, {ai.bestJ}) | Value: {value} | "
        f"Depth: {ai.depth} | Nodes: {ai.nodes_visited} | "
        f"Time: {ai.last_search_time:.3f}s"
    )
    return ai.bestI, ai.bestJ


def apply_move(ai, i, j, state):
    if not ai.isValid(i, j):
        return False
    ai.boardValue = ai.evaluate(i, j, ai.boardValue, state, ai.nextBound)
    ai.setState(i, j, state)
    ai.updateBound(i, j, ai.nextBound)
    return True


def check_human_move(ai, pos, state):
    i, j = utils.pos_pixel2map(pos[0], pos[1])
    if apply_move(ai, i, j, state):
        return i, j
    return None
