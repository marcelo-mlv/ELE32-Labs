def bit_flipping_decoder(Graph, y, max_iter=20):
    for _ in range(max_iter):
        for m in range(Graph.M):
            Graph.check_node(m, y)
        max_fails = max(Graph.vnodes_fails)
        if max_fails == 0:
            return y
        else:
            for n in range(Graph.N):
                if Graph.vnodes_fails[n] == max_fails:
                    y[n] = (y[n] + 1) % 2 # bit flip
        Graph.reset_fails()

    return y