import numpy as np
import random

def generate_parity_matrix(N, dv, dc):
    """
    Generates a parity-check matrix H for a regular LDPC code.

    Params:
        N (int): Number of variable nodes (v-nodes).
        dv (int): Number of edges per v-node.
        dc (int): Number of edges per c-node.

    Returns:
        H (np.ndarray): Parity-check matrix.
    """
    M = (N * dv) // dc  # Number of check nodes (c-nodes)
    H = np.zeros((M, N), dtype=int)

    edges = []
    for i in range(N):
        for _ in range(dv):
            edges.append(i)

    check_nodes = list(range(M)) * dc
    if len(edges) != len(check_nodes):
        raise ValueError("Invalid parameters: number of edges does not match.")

    random.shuffle(check_nodes)

    for v, c in zip(edges, check_nodes):
        while H[c, v] == 1:  # Avoid multiple connections
            c = random.choice(range(M))
        H[c, v] = 1

    return H