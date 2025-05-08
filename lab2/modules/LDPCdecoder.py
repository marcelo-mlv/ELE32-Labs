import numpy as np

def bit_flipping_decoder(Graph, y, max_iter=20):
    for _ in range(max_iter):
        for m in range(Graph.M):
            Graph.check_node(m, y)
        max_fails_idx = np.argmax(Graph.vnodes_fails)
        max_fails = Graph.vnodes_fails[max_fails_idx]
        if max_fails == 0:
            return y
        else:
            y[max_fails_idx] = (y[max_fails_idx] + 1) % 2   # bit flip, fliping only one bit 
        Graph.reset_fails()

    return y