import csv
import math
import time
from copy import deepcopy

from source.AI import GomokuAI
from source.gomoku import apply_move


TEST_STATES = {
    "Dau van": [],
    "Giua van": [
        (7, 7, 1), (7, 8, -1), (8, 7, 1), (6, 7, -1),
        (8, 8, 1), (6, 8, -1), (9, 6, 1), (5, 9, -1),
    ],
    "AI co the thang ngay": [
        (7, 6, 1), (7, 7, 1), (7, 8, 1),
        (7, 5, -1), (8, 8, -1), (6, 9, -1),
    ],
    "Nguoi sap thang can chan": [
        (7, 6, -1), (7, 7, -1), (7, 8, -1),
        (7, 5, 1), (8, 8, 1), (6, 9, 1),
    ],
    "Hai ben cung tan cong": [
        (7, 7, 1), (7, 8, -1), (8, 7, 1), (6, 8, -1),
        (9, 7, 1), (5, 8, -1), (8, 8, 1), (6, 7, -1),
    ],
}


def build_ai(moves, depth):
    ai = GomokuAI(depth=depth)
    for i, j, state in moves:
        apply_move(ai, i, j, state)
    return ai


def run_search(ai, algorithm, state=1):
    candidate = deepcopy(ai)
    candidate.ai_mode = algorithm
    candidate.nodes_visited = 0
    candidate.TTable = {}
    maximizing = state == 1
    start = time.perf_counter()
    if algorithm == "minimax":
        value = candidate.minimax(candidate.depth, candidate.boardValue, candidate.nextBound, maximizing)
    else:
        value = candidate.alphaBetaPruning(
            candidate.depth,
            candidate.boardValue,
            candidate.nextBound,
            -math.inf,
            math.inf,
            maximizing,
        )
    elapsed = time.perf_counter() - start
    return {
        "move": f"({candidate.bestI},{candidate.bestJ})",
        "value": value,
        "nodes": candidate.nodes_visited,
        "time_seconds": elapsed,
    }


def benchmark(depths=(1, 2, 3), output_path="ket_qua_thuc_nghiem.csv"):
    rows = []
    for depth in depths:
        for state_name, moves in TEST_STATES.items():
            base_ai = build_ai(moves, depth)
            mini = run_search(base_ai, "minimax")
            alpha = run_search(base_ai, "alphabeta")
            saved = 0.0
            if mini["nodes"]:
                saved = (1 - alpha["nodes"] / mini["nodes"]) * 100
            rows.append({
                "state": state_name,
                "depth": depth,
                "minimax_move": mini["move"],
                "minimax_value": mini["value"],
                "minimax_nodes": mini["nodes"],
                "minimax_time_seconds": f"{mini['time_seconds']:.6f}",
                "alphabeta_move": alpha["move"],
                "alphabeta_value": alpha["value"],
                "alphabeta_nodes": alpha["nodes"],
                "alphabeta_time_seconds": f"{alpha['time_seconds']:.6f}",
                "node_reduction_percent": f"{saved:.2f}",
                "same_move": mini["move"] == alpha["move"],
            })

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return rows


if __name__ == "__main__":
    for row in benchmark():
        print(row)
